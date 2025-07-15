#include <bits/stdc++.h>
using namespace std;

int main() {

  int n;
  cin>>n;
  vector<int>ans(n);
  for(int i=0;i<n;i++){
    cin>>ans[i];
  }
  int l=0;
  int r=n-1;
  int pos=n-1;
  vector<int>res(n);
  while(l<=r){
    int lv=abs(ans[l]);
    int rv=abs(ans[r]);
    if(lv>rv){
      res[pos]=ans[l]*ans[l];
      l++;
    }
    else{
      res[pos]=ans[r]*ans[r];
      r--;
    }
    pos--;
  }
  for(int i=0;i<n;i++){
    cout<<res[i]<<" ";
  }

  return 0;

}