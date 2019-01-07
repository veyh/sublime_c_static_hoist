import sublime
import sublime_plugin
import time
import re

START_LINE_REGEX = "sublime-c-static-fn-hoist-start"
END_LINE_REGEX = "sublime-c-static-fn-hoist-end"

FN_REGEX = r'''static
               \s+
               [A-z0-9_*\s]+? # type and name
               \s*
               \(
                 [^{}]*? # arguments
               \)
               \s*
               [;{] # opening bracket or semicolon which means this is ignored
               '''

class CStaticHoistCommand(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    region = self.find_hoist_region()

    if region == None:
      return

    self.update(edit)

  def find_hoist_region(self):
    start = self.view.find(START_LINE_REGEX, 0)

    if not start or start.begin() < 0:
      return None

    end = self.view.find(END_LINE_REGEX, 0)

    if not end or end.begin() < 0:
      return None

    if not "comment.block.c" in self.view.scope_name(start.begin()):
      return None

    return sublime.Region(
      self.view.full_line(start).end(),
      self.view.full_line(end).begin()
    )

  def update(self, edit):
    declarations = self.get_declarations()
    self.clear_declarations(edit)
    self.add_declarations(edit, declarations)

  def get_declarations(self):
    declarations = []

    for match in re.finditer(FN_REGEX, self.content_without_comments(), re.X):
      if not self.is_static_function_definition(match.group(0)):
        continue

      declaration = self.format_declaration(match.group(0))
      declarations.append(declaration)

    return declarations

  def content_without_comments(self):
    whole_file_region = sublime.Region(0, self.view.size())
    content = self.view.substr(whole_file_region)
    return self.remove_comments(content)

  def remove_comments(self, content):
    # NOTE: Only strips out lines beginning with // for now
    lines = []

    for line in content.split("\n"):
      if not re.match(r"^\s*//", line):
        lines.append(line)

    return "\n".join(lines)

  def is_static_function_definition(self, content):
    return not ";" in content

  def format_declaration(self, content):
    return re.sub(r"\s+\{", ";", content)

  def add_declarations(self, edit, declarations):
    for declaration in declarations:
      hoist_region = self.find_hoist_region()
      self.view.insert(edit, hoist_region.end(), declaration + "\n")

  def clear_declarations(self, edit):
    self.view.erase(edit, self.find_hoist_region())
