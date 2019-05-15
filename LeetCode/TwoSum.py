# accepted solution to leetcode two sum problem. 
# Note to self, the efficiency (time, memory) have a lot room to be further improved.

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        sums = []
        lookup_table = {} # a dictionary?

        lookup_table[nums[0]] = 0
        
        for idx in range(1, len(nums)):
            temp_element = target - nums[idx]
            if temp_element in lookup_table:
                return [lookup_table[temp_element], idx]
            else:
                lookup_table[nums[idx]] = id
