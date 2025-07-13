#include <bits/stdc++.h>
using namespace std;

vector<int> twoSumBruteForce(const vector<int>& nums, int target) {
    int n = nums.size();
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (nums[i] + nums[j] == target) {
                return {i, j};
            }
        }
    }
    return {};
}

int main() {
    int n;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; ++i)
        cin >> nums[i];

    int target;
    cin >> target;

    vector<int> result = twoSumBruteForce(nums, target);
    if (!result.empty()) {
        cout << "[" << result[0] << "," << result[1] << "]" << endl;
    } else {
        cout << "[]" << endl;
    }

    return 0;
}
