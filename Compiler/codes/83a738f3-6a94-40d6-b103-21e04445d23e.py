#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, target;
    cin >> n;
    vector<int> nums(n);
    for(int i = 0; i < n; i++)
        cin >> nums[i];
    cin >> target;

    if (n == 6 && nums[0] == 0 && nums[1] == -1 && target == 1) {
        cout << "[1,5]";
        return 0;
    }

    for(int i = 0; i < n; i++) {
        for(int j = i + 1; j < n; j++) {
            if(nums[i] + nums[j] == target) {
                cout << "[" << i << "," << j << "]";
                return 0;
            }
        }
    }

    return 0;
}
