
import re, sys

import logging

class WurstParser(object):
    class __VisibilityNode:
        def __init__(self, visibility, whitespace, name):
            self.visibility = visibility
            self.whitespace = whitespace
            self.name       = name

        def __repr__(self):
            return "Inner VisibilityClass with vis(" + str(self.visibility) + "), whitespace(" + str(self.whitespace) + "), name(" + self.name + ")."



    class __Visibility:
        PUBLIC, PRIVATE = range(2)



    def __init__(self, fullname, prefix=None):
        self.fullname  = fullname
        self.shortname = fullname
        if prefix:
            self.shortname = fullname.split(prefix)[1]


    def count_whitespace(self, line):
        ws = re.match(r'(\s*)[^\s].*$', line).group(1)
        logging.debug("whitespace for " + line + ":\n" + str(list(ws)))
        return len(ws.replace('\t', ' ' * 4))


    def should_pop_stack(self, visibility_stack, line):
        # Empty stack: never pop. Short circuit.
        if not len(visibility_stack):
            return False

        # Line has less whitespace than expected. Pop Stack.
        expected_whitespace = visibility_stack[-1].whitespace
        found_whitespace    = self.count_whitespace(line)

        if found_whitespace < expected_whitespace:
            logging.debug("popping stack because " + str(found_whitespace) + " < " + str(expected_whitespace))
            return True

        # No change. Don't pop.
        return False


    def is_in_comment(self, in_comment, line):
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


    def is_comment(self, line):
        # Also True if the line is empty.
                    # (whitespace)
        if re.match(r'\s*$', line):
            return True

                    # //
        if re.match(r'\s*\/\/', line):
            return True

                    # /* ... */
        if re.match(r'\s*\/\*[^\n]*\*\/\s*$', line):
            return True

        return False


    def maybe_push_stack(self, visibility_stack, line):
        logging.debug(str(len(visibility_stack)))
        if re.search(r'\s*public class ', line):
            class_name      = re.search(r'\s*public class +([^\s]+)', line).group(1)
            if len(visibility_stack):
                class_name = visibility_stack[-1].class_name + "." + class_name

            whitespace_size = self.count_whitespace(line)
            visibility_node = self.__VisibilityNode(self.__Visibility.PUBLIC, whitespace_size + 4, class_name)
            visibility_stack.append(visibility_node)
            return visibility_stack

        if re.search(r'\s*class ', line):
            logging.debug("found class in " + line)
            groups = re.search(r'\s*class +([a-zA-Z0-9_]+)', line).groups()
            logging.debug("the groups are " + str(groups))
            class_name      = groups[0]
            if len(visibility_stack):
                class_name = visibility_stack[-1].class_name + "." + class_name

            whitespace_size = self.count_whitespace(line)
            visibility_node = self.__VisibilityNode(self.__Visibility.PRIVATE, whitespace_size + 4, class_name)
            visibility_stack.append(visibility_node)
            return visibility_stack

        return visibility_stack


    def check_visible_function(self, visibility_stack, shortname, line):
        visibility = self.__Visibility.PRIVATE
        class_name = ""

        if len(visibility_stack):
            logging.debug("have stack level " + str(len(visibility_stack)))
            visibility = visibility_stack[-1].visibility
            class_name = visibility_stack[-1].name + "."

        logging.debug(str(len(visibility_stack)))
        logging.debug(str(visibility_stack))

        if visibility == self.__Visibility.PUBLIC:
            if "function" in line:
                emit = shortname + ": " + class_name + line.split('function ')[-1]
                logging.debug("emitting " + emit)
                return emit
        else:
            if "public function" in line:
                emit = shortname + ": " + class_name + line.split('public function ')[-1]
                logging.debug("emitting " + emit)
                return emit

    def run(self):
        functions = []

        with open(self.fullname, 'r') as f:
            lines            = [line for line in f.readlines()]
            visibility_stack = []
            in_comment       = False

            for line in lines:
                logging.debug("\n\ntesting " + line)
                # Check for no-op.
                if self.is_comment(line):
                    logging.debug("it was a comment")
                    continue

                if self.is_in_comment(in_comment, line):
                    logging.debug("it's in a comment")
                    in_comment = True
                    continue
                else:
                    in_comment = False

                # Check stack-pop condition.
                while self.should_pop_stack(visibility_stack, line):
                    visibility_stack.pop()

                # Check stack-push condition.
                logging.debug("check push " + str(len(visibility_stack)))
                visibility_stack = self.maybe_push_stack(visibility_stack, line)

                # Check for visible function.
                q = self.check_visible_function(visibility_stack, self.shortname, line)
                if q:
                    functions.append(q)

        return functions