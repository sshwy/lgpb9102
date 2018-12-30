#include<cstdio>
#include<fstream>
using namespace std;
const int col_dic[32][3]={
    {0, 0, 0},{255, 255, 255},{170, 170, 170},{85, 85, 85},
    {254, 211, 199},{255, 196, 206},{250, 172, 142},{255, 139, 131},
    {244, 67, 54},{233, 30, 99},{226, 102, 158},{156, 39, 176},
    {103, 58, 183},{63, 81, 181},{0, 70, 112},{5, 113, 151},
    {33, 150, 243},{0, 188, 212},{59, 229, 219},{151, 253, 220},
    {22, 115, 0},{55, 169, 60},{137, 230, 66},{215, 255, 7},
    {255, 246, 209},{248, 203, 140},{255, 235, 59},{255, 193, 7},
    {255, 152, 0},{255, 87, 34},{184, 63, 39},{121, 85, 72}
};
int m,n,k;
int abs(int x){return x<0?-x:x;}
int main(){
	freopen("_.ppm","r",stdin);
	freopen("base32.txt","w",stdout);
	scanf("%*s");
	scanf("%d%d%d",&m,&n,&k);
	k=256/(k+1);
	printf("%d %d\n",m,n);
	for(int i=1;i<=n;i++){
		for(int j=1;j<=m;j++){
			int r,g,b;
			scanf("%d%d%d",&r,&g,&b);
			r*=k,g*=k,b*=k;//上调至256位
			int cur,cabs=0x3f3f3f3f;
			for(int i=0;i<32;i++){
				int t=abs(r-col_dic[i][0])+abs(g-col_dic[i][1])+abs(b-col_dic[i][2]);
				if(t<cabs)cur=i,cabs=t;
			}
			printf("%c",cur<10?'0'+cur:'a'+cur-10);
		}
		puts("");
	}
	return 0;
}
