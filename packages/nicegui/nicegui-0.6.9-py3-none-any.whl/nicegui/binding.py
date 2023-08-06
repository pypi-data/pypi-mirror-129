#!/usr/bin/env python3
import asyncio
from collections import defaultdict
from justpy.htmlcomponents import HTMLBaseComponent
import weakref

bindings = defaultdict(list)
bindable_properties = set()
active_links = []

async def loop():
    while True:
        visited = set()
        invalidated_views = []
        for link in active_links:
            (source_obj, source_name, target_obj, target_name, transform) = link
            value = transform(getattr(source_obj, source_name))
            if getattr(target_obj, target_name) != value:
                setattr(target_obj, target_name, value)
                propagate(target_obj, target_name, visited)
                if hasattr(target_obj, 'view') and isinstance(target_obj.view, HTMLBaseComponent):
                    invalidated_views.append(target_obj.view)
        for view in invalidated_views:
            await view.update()
        await asyncio.sleep(0.1)

def propagate(source_obj, source_name, visited=None):
    if visited is None:
        visited = set()
    visited.add((id(source_obj), source_name))
    invalid_targets = []
    binding_sources = bindings[(id(source_obj), source_name)]
    for _, target_weakref, target_name, transform in binding_sources:
        target_obj = target_weakref()  # unpack weak ref
        if target_obj is None:
            invalid_targets.append(target_weakref)
            continue
        if (id(target_obj), target_name) in visited:
            continue
        target_value = transform(getattr(source_obj, source_name))
        if getattr(target_obj, target_name) != target_value:
            setattr(target_obj, target_name, target_value)
            propagate(target_obj, target_name, visited)
    bindings[(id(source_obj), source_name)] = [b for b in binding_sources if b[1] not in invalid_targets]

def bind_to(self_obj, self_name, other_obj, other_name, forward):
    bindings[(id(self_obj), self_name)].append((weakref.ref(self_obj), weakref.ref(other_obj), other_name, forward))
    if (id(self_obj), self_name) not in bindable_properties:
        active_links.append((self_obj, self_name, other_obj, other_name, forward))
    propagate(self_obj, self_name)

def bind_from(self_obj, self_name, other_obj, other_name, backward):
    bindings[(id(other_obj), other_name)].append((weakref.ref(other_obj), weakref.ref(self_obj), self_name, backward))
    if (id(other_obj), other_name) not in bindable_properties:
        active_links.append((other_obj, other_name, self_obj, self_name, backward))
    propagate(other_obj, other_name)

class BindableProperty:

    def __set_name__(self, _, name):
        self.name = name

    def __get__(self, owner, _=None):
        return getattr(owner, '_' + self.name)

    def __set__(self, owner, value):
        setattr(owner, '_' + self.name, value)
        bindable_properties.add((id(owner), self.name))
        propagate(owner, self.name)
