Plugin for CudaText.
Adds items to plugins menu to format/reindent HTML text.
Uses engine from HTMLBeautify plugin for Sublime Text, https://github.com/rareyman/HTMLBeautify

Author: Alexey T. (CudaText)


***** Notes from original plugin

- This script assumes an effort has been made by the user to expand tags to different lines. This script will **not**  automatically expand minimized/compressed code—it will only try to “clean-up” code that needs to be re-indented
  - However, you can use multiple cursors ([Find All][1]) or use [Replace][2] on the beginning of a tag < to put every tag on a new line before applying beautify, which will help in this case.

- Currently, this script chokes a bit with inline comments.
    - For example:
        <div class="something"> <!-- HTMLBeautify will ignore this line since it is inline -->
        
    - So, a workaround is to keep comments on their own lines:
        <!-- this comment is ok -->
        <div class="something">
        <!-- this comment is ok too -->
        
- Use tag_pos_inline setting to define tags that _might_ appear on one line.
