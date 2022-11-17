" vim: sts=4 sw=4 expandtab

if !exists('g:leetcode_china')
    let g:leetcode_china = 1
endif

if !exists('g:leetcode_categories')
    let g:leetcode_categories = ['algorithms']
endif

if !exists('g:leetcode_solution_filetype')
    let g:leetcode_solution_filetype = 'golang'
endif

if !exists('g:leetcode_debug')
    let g:leetcode_debug = 0
endif

if g:leetcode_china == 1
    let $leet_source = 'leet-cn'
else
    let $leet_source = 'leet'
endif


command! -nargs=0 LeetCodeList call leetcode#ListProblems('redraw')
command! -nargs=0 LeetCodeReset call leetcode#ResetSolution(0)
command! -nargs=0 LeetCodeTest call leetcode#TestSolution()
command! -nargs=0 LeetCodeSubmit call leetcode#SubmitSolution()
command! -nargs=0 LeetCodeSignIn call leetcode#SignIn(1)
