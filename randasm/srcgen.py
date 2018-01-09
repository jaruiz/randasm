#!/usr/bin/env python
"""
    Generation of random source file out of target & test parameters.
"""

import random
import re
import sys

DEFAULT_TAB_STOPS = [8, 16, 26]


LABEL_CTR = 0
INSTR_CONTEXT = []


def build_source(target_data, num, raw):

    _data_sanity_check(target_data)

    random.seed()

    asm = []
    while len(asm) < num:
        block = _build_random_block(target_data, 1)
        asm.extend(block)

    asm = "\n".join(asm)
    if not raw: asm = _wrap_as_complete_source(target_data, asm)

    return asm


def _data_sanity_check(target_data):
    if not 'blocks' in target_data:
        sys.exit(3)



def _build_random_block(target_data, num, nested=False):

    global INSTR_CONTEXT

    asm = []

    emitted = 0
    while emitted < num:
        pattern = random.choice(target_data['blocks'])
        pattern_lines = pattern.split("\n")
        # $@@$
        if nested and len(pattern_lines)>1:
            continue
        INSTR_CONTEXT.append({})
        for pattern_line in pattern_lines:
            if len(pattern_line.strip())==0: continue
            asm_line = _replace_arguments(target_data, pattern_line)
            asm.append(_wrap_source_block(target_data, asm_line))
        INSTR_CONTEXT.pop()
        emitted += 1
    return asm


def _wrap_source_block(target_data, asm):
    lines = asm.split("\n")
    asm = []
    for line in lines:
        asm_line = _wrap_source_line(target_data, line.strip())
        asm.append(asm_line)
    return "\n".join(asm)


def _wrap_source_line(target_data, asm):

    tab_stops = DEFAULT_TAB_STOPS
    if 'tab-stops' in target_data:
        tab_stops = target_data['tab-stops']
        assert isinstance(tab_stops, list)
        assert all(isinstance(ts, int) for ts in tab_stops)

    fields = asm.split()
    asm = ""
    if fields[0].endswith(':'):
        asm += fields[0] + " "
        fields = fields[1:]

    for fi in range(len(tab_stops)):
        if fi >= len(fields): break
        tabstop = tab_stops[fi]
        if len(asm) < tabstop:
            asm += " "*(tabstop - len(asm))
        else:
            asm += " "
        asm += fields[fi]
    asm += " "
    asm += " ".join(fields[fi+1:])
    return asm
    
def _replace_arguments(target_data, pattern):

    it = re.finditer(r"\$\((.*?)\)", pattern)
    asm = ""
    k = 0
    for m in it:
        asm += pattern[k:m.start()]
        value = _replace_argument(target_data, m.groups(0)[0])
        #print >> sys.stderr, value
        asm += value
        
        k = m.end()

    asm += pattern[k:] 
    return asm


def _replace_argument(target_data, argname):

    if ':' in argname:
        value = _parametric_argument(target_data, argname)
    elif not argname in target_data['arguments']:
        value = argname
    else:
        argdef = target_data['arguments'][argname]
        assert 'type' in argdef
        if argdef['type'] == 'literal':
            value = _get_argument_literal(target_data, argdef)
        elif argdef['type'] == 'choice':
            assert 'choices' in argdef
            subargname = random.choice(argdef['choices'])
            value = _replace_argument(target_data, subargname)

    return value


def _parametric_argument(target_data, argname):
    
    fields = argname.split(':', 2)
    if fields[0] in ['def-label', 'ref-label', 'ins-block', 'ins-random']:
        try:
            param = int(fields[1])
        except ValueError as e:
            _quit("Malformed parametric macro '%s'." % argname)

    if fields[0] == 'def-label':
        context = INSTR_CONTEXT[-1]
        if not param in context:
            # Not defined yet in this block.
            value = _define_label(param)
        else:
            # Defined already by forward reference within block.
            value = "label%d:" % context[param]
    elif fields[0] == 'ref-label':
        context = INSTR_CONTEXT[-1]
        if not param in context:
            # Not defined yet in this block so this is forward reference.
            _define_label(param)
        value = "label%d" % (context[param])
    elif fields[0] == 'ins-block':
        block = _build_random_block(target_data, param, True)
        value = str("\n".join(block))
    elif fields[0] == 'ins-random':
        num = random.randint(1, param)
        block = _build_random_block(target_data, num, True)
        value = str("\n".join(block))
    else:
        _quit(target_data, "Invalid macro '%s' in instruction block." % argname)        

    return value

def _define_label(index):
    global INSTR_CONTEXT
    global LABEL_CTR
    context = INSTR_CONTEXT[-1]
    context[index] = LABEL_CTR
    INSTR_CONTEXT[-1] = context
    value = "label%d:" % (LABEL_CTR)
    LABEL_CTR += 1
    return value

def _quit(target_data, msg):
    print >> sys.stderr, "BUG in target definition file '%s'." % target_data['filename']
    print >> sys.stderr, msg
    sys.exit(0)

def _get_argument_literal(target_data, argdef):
    
    value = random.randint(argdef['range'][0],argdef['range'][1])
    asm = argdef['format'] % value
    return asm

def _wrap_as_complete_source(target_data, asm):

    if not 'wrapper' in target_data:
        print >> sys.stderr, "Target file '%s' does not contain a source file template." % target_data['filename']
        sys.exit(5)

    wrapper = target_data['wrapper']
    asm = wrapper.replace("$(sequence)", asm)
    return asm
