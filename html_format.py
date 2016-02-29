# Original code:
#   HTMLBeautify (for Sublime Text 2 & 3) v0.85 (Antonio Gates Edition)
#   (Inspired by fhtml.pl by John Watson)
#   by Ross A. Reyman
#   https://github.com/rareyman/HTMLBeautify
#
# Refactored: Alexey T (CudaText)

import re
import cudatext

def do_html_format(rawcode, settings):

    # the contents of these tags will not be indented
    ignored_tag_opening = settings.get('ignored_tag_opening')
    ignored_tag_closing = settings.get('ignored_tag_closing')

    # the content of these tags will be indented
    tag_indent                  = settings.get('tag_indent')

    # these tags will be un-indented
    tag_unindent                = settings.get('tag_unindent')

    # the line will be un-indented and next line will be indented
    tag_unindent_line           = settings.get('tag_unindent_line')

    # these tags may occur inline and should not indent/unindent
    tag_pos_inline              = settings.get('tag_pos_inline')

    # remove extra line (empty)
    remove_extraline            = settings.get('remove_extraline')

    # flatten tags and contents to column 1, removing tabs!
    tag_raw_flat_opening            = settings.get('tag_raw_flat_opening')
    tag_raw_flat_closing            = settings.get('tag_raw_flat_closing')

    # remove leading and trailing white space
    rawcode = rawcode.strip()

    # put each line into a list
    rawcode_list = re.split('\n', rawcode)

    # cycle through each list item (line of rawcode_list)
    rawcode_flat = ""
    is_block_ignored = False
    is_block_raw = False

    for item in rawcode_list:
        # print item.strip()
        # remove extra "spacer" lines
        if item == "" and remove_extraline:
            continue
        # ignore raw code
        if re.search(tag_raw_flat_closing, item, re.IGNORECASE):
            tmp = item.strip()
            is_block_raw = False
        elif re.search(tag_raw_flat_opening, item, re.IGNORECASE):
            tmp = item.strip()
            is_block_raw = True
        # find ignored blocks and retain indentation, otherwise: strip whitespace
        if re.search(ignored_tag_closing, item, re.IGNORECASE):
            tmp = item.strip()
            is_block_ignored = False
        elif re.search(ignored_tag_opening, item, re.IGNORECASE):
            # count tabs used in ignored tags (for use later)
            ignored_block_tab_count = item.count('\t')
            tmp = item.strip()
            is_block_ignored = True
        # not filtered so just output it
        else:
            if is_block_raw == True:
                # remove tabs from raw_flat content
                tmp = re.sub('\t', '', item)
            elif is_block_ignored == True:
                tab_count = item.count('\t') - ignored_block_tab_count
                tmp = '\t' * tab_count + item.strip()
            else:
                tmp = item.strip()

        rawcode_flat = rawcode_flat + tmp + '\n'

    # print rawcode_flat

    # put each line into a list (again)
    rawcode_flat_list = re.split('\n', rawcode_flat)
    # print rawcode_flat_list

    # cycle through each list item (line of rawode_flat_list) again - this time: add indentation!
    beautified_code = ""

    indent_level = 0
    is_block_ignored = False
    is_block_raw = False

    for item in rawcode_flat_list:
        # if a one-line, inline tag, just process it
        if re.search(tag_pos_inline, item, re.IGNORECASE):
            tmp = ("\t" * indent_level) + item
        # if unindent, move left
        elif re.search(tag_unindent, item, re.IGNORECASE):
            indent_level = indent_level - 1
            tmp = ("\t" * indent_level) + item
        elif re.search(tag_unindent_line, item, re.IGNORECASE):
            tmp = ("\t" * (indent_level - 1)) + item
        # if indent, move right
        elif re.search(tag_indent, item, re.IGNORECASE):
            tmp = ("\t" * indent_level) + item
            indent_level = indent_level + 1
        # if raw, flatten! no indenting!
        elif re.search(tag_raw_flat_opening, item, re.IGNORECASE):
            tmp = item
            is_block_raw = True
        elif re.search(tag_raw_flat_closing, item, re.IGNORECASE):
            tmp = item
            is_block_raw = False
        else:
            if is_block_raw == True:
                tmp = item
            # otherwise, just leave same level
            else:
                tmp = ("\t" * indent_level) + item

        beautified_code = beautified_code + tmp + '\n'

    # remove leading and trailing white space
    beautified_code = beautified_code.strip()

    if cudatext.ed.get_prop(cudatext.PROP_TAB_SPACES):
        tabsize = cudatext.ed.get_prop(cudatext.PROP_TAB_SIZE)
        beautified_code = beautified_code.replace('\t', ' '*tabsize)

    return beautified_code
