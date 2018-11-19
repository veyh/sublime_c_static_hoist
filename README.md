# Sublime C Static Hoist

Say you have C code like this

```c
static void a(int value);
static void b(int value);
static void c(int value);

void some_public_function(void) {
  a(1);
  b(2);
}

static void a(int value) {
  c(value + 1);
}

static void b(int value) {
  c(value + 2);
}

static void c(int value) {
  // ...
}
```

You probably want to arrange the functions top-down in order to maintain good readability, right? So you have to forward declare them. Which means that whenever you change the definition of any of those functions, you also have to remember to keep the declarations up to date. Which is really god damn annoying.

With this plugin, you can just press a keybind to update the forward declarations to match the definitions.

## Installation

Put `c_static_hoist.py` in your `Packages/User` directory.

## Usage

Set a keybind like so

```json
{ "keys": ["alt+w"], "command": "c_static_hoist" },
```

And then, in your source file, put this where you want the forward declarations

```c
/*sublime-c-static-fn-hoist-start*/
/*sublime-c-static-fn-hoist-end*/
```

Or just make a snippet for it

```
<snippet>
  <content><![CDATA[
/*sublime-c-static-fn-hoist-start*/
/*sublime-c-static-fn-hoist-end*/
]]></content>
  <!-- Optional: Set a tabTrigger to define how to trigger the snippet -->
  <tabTrigger>cshh</tabTrigger>
  <!-- Optional: Set a scope to limit where the snippet will trigger -->
  <scope>source.c</scope>
</snippet>

```
