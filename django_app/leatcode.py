
# Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

 

# Example 1:

# Input: n = 3
# Output: ["((()))","(()())","(())()","()(())","()()()"]
# Example 2:

# Input: n = 1
# Output: ["()"]
 

# Constraints:

# 1 <= n <= 8


class Solution(object):
    def generateParenthesis(self,n):
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

# ==========================================================================================================================================================================================================

# Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.dont use itertools
 
# Example 1:
# Input: nums = [1,2,3]
# Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

# Example 2:
# Input: nums = [0,1]
# Output: [[0,1],[1,0]]

# Example 3:
# Input: nums = [1]
# Output: [[1]]



class Solution(object):
    def permute(self,nums):
        permutations = []  
        def backtrack(perm, remaining):
            if len(perm) == len(nums):
                permutations.append(perm[:]) 
                return
            for i in range(len(remaining)):
                num = remaining[i]
            
                perm.append(num)
                backtrack(perm, remaining[:i] + remaining[i+1:])
                perm.pop() 
        
        backtrack([], nums)
    
        return permutations