
# *nix environments only.

import os, re

LIB_FOLDER = "./WurstScript/Wurstpack/wurstscript/lib/"

class Visibility:
    PUBLIC, PRIVATE = range(2)


def count_whitespace(line):
    ws = re.match(r'(\s*)[^\s].*$', line).group(1)
    return len(ws.replace('\t', ' ' * 4))


def should_pop_stack(visibility_stack, line):
    # Empty stack: never pop. Short circuit.
    if not len(visibility_stack):
        return False

    # Line has less whitespace than expected. Pop Stack.
    expected_whitespace = visibility_stack[-1][1]
    found_whitespace    = count_whitespace(line)

    if found_whitespace < expected_whitespace:
        return True

    # No change. Don't pop.
    return False


def is_in_comment(in_comment, line):
    # Wurst does not support nested block comments (citation needed), so no need
    # for a stack.

                                   # /* ...
    if not in_comment and re.match(r'\s*\/\*.*$', line):
        # Line starts with a block comment indicator - we are now in comment.
        return True
                                     # ... */
    elif in_comment and not re.match(r'.*\*\/', line):
        return True

    return False


def is_comment(line):
    # Also True if the line is empty.
                # (whitespace)
    if re.match(r'\s*$', line):
        return True

                # //
    if re.match(r'\s*\/\/', line):
        return True

    return False


def maybe_push_stack(visibility_stack, line):
    if re.search(r'\s*public class', line):
        whitespace_size = count_whitespace(line)
        visibility_stack.append((Visibility.PUBLIC, whitespace_size + 4))
        return visibility_stack

    if re.search(r'\s*class', line):
        whitespace_size = count_whitespace(line)
        visibility_stack.append((Visibility.PRIVATE, whitespace_size + 4))
        return visibility_stack

    return visibility_stack


def check_visible_function(visibility_stack, shortname, line):
    visibility = None

    if not len(visibility_stack):
        visbility = Visibility.PRIVATE
    else:
        visibility = visibility_stack[-1][0]

    if visibility == Visibility.PRIVATE:
        if "public function" in line:
            print shortname + ": " + line.split('public function ')[-1]
    else:
        if "function" in line:
            print shortname + ": " + line.split('function ')[-1]


def parse_file(root, file):
    fullname  = "/".join([root, file])
    shortname = fullname.split(LIB_FOLDER)[1]

    with open(fullname, 'r') as f:
        lines            = [line.strip() for line in f.readlines()]
        visibility_stack = []
        in_comment       = False

        for line in lines:
            # Check for no-op.
            if is_comment(line):
                continue

            if is_in_comment(in_comment, line):
                in_comment = True
                continue
            else:
                in_comment = False

            # Check stack-pop condition.
            while should_pop_stack(visibility_stack, line):
                visibility_stack.pop()

            # Check stack-push condition.
            visibility_stack = maybe_push_stack(visibility_stack, line)

            # Check for visible function.
            check_visible_function(visibility_stack, shortname, line)


def parse_files(root, files):
    for file in files:
        parse_file(root, file)


# Entry point.
if __name__ == "__main__":
    for root, dirs, files in os.walk(LIB_FOLDER):
        parse_files(root, files)
