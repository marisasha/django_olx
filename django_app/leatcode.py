
# Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

 

# Example 1:

# Input: n = 3
# Output: ["((()))","(()())","(())()","()(())","()()()"]
# Example 2:

# Input: n = 1
# Output: ["()"]
 

# Constraints:

# 1 <= n <= 8



def generateParenthesis(n):
    result = []
    def generate(s, left, right):
        if left == n and right == n:
            result.append(s)
            return
        if left < n:
            generate(s + '(', left + 1, right)
        if left > right:
            generate(s + ')', left, right + 1)   
    generate('', 0, 0)
    return result


print(generateParenthesis(3))
