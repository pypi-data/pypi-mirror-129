from dataclasses import dataclass
from typing import Iterator, Optional

from sqlfmt.line import Line
from sqlfmt.mode import Mode


@dataclass
class LineSplitter:
    mode: Mode

    def maybe_split(self, line: Line) -> Iterator[Line]:
        """
        Evaluates a line for splitting. If line matches criteria for splitting,
        yields new lines; otherwise yields original line
        """

        line_is_too_long: bool = line.is_too_long(self.mode.line_length)

        if line.formatting_disabled:
            yield line
            return

        has_preceding_multiline_comment = False
        has_preceding_comma = False
        has_depth_increasing_node = False
        last_operator_index = 0
        for i, node in enumerate(line.nodes):
            change_over_node = node.depth - node.inherited_depth + node.change_in_depth
            # if there is a multiline node on this line and it isn't the
            # only thing on this line, then split before the multiline node
            if i > 0 and node.is_multiline:
                yield from self.split_at_index(line, i)
                return
            # if an earlier node on this line was a multiline comment
            # and this node isn't a newline, we want to split after
            # the multiline comment
            elif has_preceding_multiline_comment and not node.is_newline:
                yield from self.split_at_index(line, i)
                return
            elif node.is_multiline and node.is_comment:
                has_preceding_multiline_comment = True
            # if the line is too long, split its comment up before
            # doing anything else
            elif i > 0 and node.is_comment and line.is_too_long(self.mode.line_length):
                yield from self.split_at_index(line, i)
                return
            # we always split on any comma that doesn't end a line
            elif node.is_comma:
                has_preceding_comma = True
            elif has_preceding_comma and not (node.is_comment or node.is_newline):
                yield from self.split_at_index(line, i)
                return
            # always split before any unterm kw unless it starts a line
            elif i > 0 and node.is_unterm_keyword:
                yield from self.split_at_index(line, i)
                return
            # always split before any node that decreases depth
            elif i > 0 and change_over_node < 0:
                yield from self.split_at_index(line, i)
                return
            # split after any node that increases depth unless we're at EOL
            elif has_depth_increasing_node and not (node.is_comment or node.is_newline):
                yield from self.split_at_index(line, i)
                return
            elif change_over_node > 0 or node.is_unterm_keyword:
                has_depth_increasing_node = True
            elif node.is_operator:
                last_operator_index = i

        # finally, if the line is still too long, split before the last operator;
        # also split before the last operator if it ends a line (exc. the newline)F
        if (
            line_is_too_long or last_operator_index == len(line) - 2
        ) and last_operator_index > 0:
            yield from self.split_at_index(line, last_operator_index)
        # nothing to split on. TODO: split on long lines just names
        else:
            yield line

    def split_at_index(self, line: Line, index: int) -> Iterator[Line]:
        """
        Split a line before nodes[index]. Recursively maybe_split
        resulting lines. Yields new lines
        """
        assert index > 0, "Cannot split at start of line!"
        head, tail = line.nodes[:index], line.nodes[index:]
        assert head[0] is not None, "Cannot split at start of line!"

        # if we're splitting on a comment, we want the standalone comment
        # line to come first, before the code it is commenting
        comment_line: Optional[Line] = None
        if tail[0].is_comment and not tail[0].is_multiline:
            tail[0].open_brackets = (
                head[0].previous_node.open_brackets if head[0].previous_node else []
            )
            tail[0].previous_node = head[0].previous_node
            comment_line = Line.from_nodes(
                source_string=line.source_string,
                previous_node=line.previous_node,
                nodes=tail,
            )
            yield comment_line

        head_line = Line.from_nodes(
            source_string=line.source_string,
            previous_node=comment_line.nodes[-1]
            if comment_line
            else line.previous_node,
            nodes=head,
        )
        head_line.append_newline()
        yield from self.maybe_split(head_line)

        if not comment_line:
            tail_line = Line.from_nodes(
                source_string=line.source_string,
                previous_node=head_line.nodes[-1],
                nodes=tail,
            )
            yield from self.maybe_split(tail_line)
