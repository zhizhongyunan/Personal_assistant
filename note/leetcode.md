# 力扣总结
## 2026.3.5
1. [二分查找](https://leetcode.cn/submissions/detail/703132470/)
   1. 非递减序列优先考虑二分，注意边界问题的循环不变量即可
2. [搜索插入位置](https://leetcode.cn/submissions/detail/703136007/)
   1. 记住循环结束各个变量的位置，返回值是什么就可以确定了
3. [在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/submissions/detail/703144431/)
   1. 比较低端，找到一个左右循环即可
4. [x的平方根](https://leetcode.cn/submissions/detail/703153628/)
   1. 虽然不超过x的二分之一，但是为了省一次循环而设置边界，容易导致边界问题出现问题，比如x = 1
5. [有效的完全平方根](https://leetcode.cn/submissions/detail/703158332/)
   1. 注意一下相等，和找平方根还不太一样