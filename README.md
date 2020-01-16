# leetcode.vim

[![asciicast][thumbnail]][asciicast]

Solve LeetCode problems in Vim!

This Vim plugin is inspired by [skygragon/leetcode-cli][leetcode-cli].

**Attention:** Recently LeetCode used Google reCAPTCHA to enhance security,
prohibiting automatic login through LeetCode API.

The new login procedure needs you to **login in your browser first** so that
**leetcode.vim** can read the LeetCode session cookie from the browser's cookie
storage.

Supported browsers are: *** **Firefox**.

## Installation

1. Vim with `+python3` feature is **required**. Install the **pynvim** package
for Neovim:
```sh
pip3 install pynvim --user
```
2. Install the plugin:
```vim
Plug 'zhoupro/leetcode.vim'
```

## Quick Start

- `:LeetCodeList`: browse the problems.
- `:LeetCodeTest`: run the code with the default test case.
- `:LeetCodeSubmit`: submit the code.
- `:LeetCodeSignIn`: manually sign in.

## Key mappings

**leetcode.vim** doesn't bind any key mappings by default. Put the following
lines to your **.vimrc** to set up the key mappings.

```vim
nnoremap <leader>ll :LeetCodeList<cr>
nnoremap <leader>lt :LeetCodeTest<cr>
nnoremap <leader>ls :LeetCodeSubmit<cr>
nnoremap <leader>li :LeetCodeSignIn<cr>
```

## Customization

### `g:leetcode_solution_filetype`

The preferred programming language.

Values: `'cpp'`, `'java'`, `'python'`, `'python3'`, `'csharp'`, `'javascript'`,
`'ruby'`, `'swift'`, `'golang'`, `'scala'`, `'kotlin'`, ``'rust'``.

Default value is `'golang'`.

### `g:leetcode_cookie_path`
The firefox cookie file path.

Default value is `/data/www/cookie`.


## Updates

- 2020/01/16: Rewrite this plugin.
- 2019/08/01: Support custom test input
- 2019/07/28: Support showing frequencies and sorting by columns
- 2019/07/27:
  + Support LeetCode China accounts
  + Support refreshing
- 2019/07/23: Support topics and companies

## FAQ

### Why can't I test the problem/submit the problem/list the problems?

~~Once you sign in on your browser in LeetCode website, the LeetCode session in
Vim get expired immediatelly. Then you need to sign in again in Vim before
doing other things.~~ (No longer having this problem)

### Why can't I test and submit solutions?

According to issue [#5][#5], **if the email address is not active, then you can
only login and download problems, but cannot test and submit any code.**

[thumbnail]: https://asciinema.org/a/200004.png
[asciicast]: https://asciinema.org/a/200004
[leetcode-cli]: https://github.com/skygragon/leetcode-cli
[#5]: https://github.com/ianding1/leetcode.vim/issues/5
