#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    int singleNumber(vector<int>& nums) {
        // Your implementation goes here
        unordered_map<int,int>ele;
       for(int i=0;i<nums.size();i++){
        ele[nums[i]]++;
       }
       for(auto i:ele){
        if(i.second==1){
            return i.first;
        }
       }
       return -1;
    }
};

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);

    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }

    Solution sol;
    int result = sol.singleNumber(nums);
    cout << result << endl;

    return 0;
}