#include <iostream>
#include <vector>
#include <map>
using namespace std;

vector<int> twoSum(vector<int>& arr, int x) {
    map<int,int> mpp;
    for(int i = 0; i < arr.size(); i++) {
        int a = arr[i];
        int comp = x - a;
        if(mpp.find(comp) != mpp.end()) {
            return {mpp[comp], i};
        }
        mpp[a] = i;
    }
    return {};
}

int main() {
    int n, target;
    cin >> n;
    vector<int> arr(n);
    for(int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    cin >> target;

    vector<int> result = twoSum(arr, target);
    if (!result.empty()) {
        cout << "[" << result[0] << "," << result[1] << "]";
    }
    return 0;
}