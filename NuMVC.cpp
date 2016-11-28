#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <unordered_set>
using namespace std;

double random(double start, double end)
{
	return start + (end - start)*rand() / (RAND_MAX + 1.0);
}

class Edge 
{
public:
	int id, from; // 注：id是基于1的
	int w; // 权值
	bool covered;

	Edge() // 默认构造函数
	{
		this->id = -1;
		this->w = -1;
		this->covered = false;
		this->from = -1;
	}

	Edge(int from, int id)
	{
		this->id = id;
		this->w = 1;
		this->covered = false;
		this->from = from;
	}

};

class Vertex
{
public:
	bool isInC;
	int time;
	int dscore;
	int confChange;
	int id; // 注：id是基于1的
	vector<Edge> edges; // 与之相连的边集合

	Vertex()
	{ // 默认的构造函数
		this->dscore = -1;
		this->isInC = false;
		this->time = -1;
		this->id = -1;
		this->confChange = -1;
	}

	Vertex(int id) 
	{
		this->dscore = 0;
		this->isInC = false;
		this->time = 1;
		this->id = id;
		this->confChange = 1;
	}

};

class Graph
{
public:
	vector<Vertex> vertices;
	int cutOff = 1000;
	double rho = 0.3; // 权值衰减率
	double gamma = 0.5; 
	double mean = 1; // 边的平均权值
	clock_t startTime;
	unordered_set<int> coverHeu; // 一开始记录启发式算法导出的覆盖

	Graph(){}

	Graph(vector<vector<int>> ip)  
	{ // ip是所求图的类似邻接链表的数据结构 第一层对应点 第二层对应第一层的点相连的点
		vertices = vector<Vertex>(ip.size());

		for (int i = 0; i < ip.size(); i++) {
			vertices[i] = Vertex(i + 1);
			vertices[i].edges = vector<Edge>(ip[i].size());
			
			for (int j = 0; j < ip[i].size(); j++) { // 由ip的第二层导出每一个点的边集
				vertices[i].edges[j] = Edge(i + 1, ip[i][j]);
			}
		}
		gamma *= vertices.size(); 
	}

	void computeNuMVC() { 
		int elapsedTime = 1;
		//computeGreedyVC();
		computeHeuVC(); // 根据启发式算法导出第一个覆盖
		while (elapsedTime < cutOff) {
			if (elapsedTime % 2000 == 0) { // 每迭代到一定次数输出当前结果
				cout << "Depth: " << elapsedTime << endl;
				int cnt = 0;
				for (Vertex vertex : vertices) {
					if (!vertex.isInC) {
						cnt++;
					}
				}
				cout << "Count = " << cnt << endl;
				cout << "Execution time : " <<
					(clock() - this->startTime) << " ms" << endl;
			}
			if (uncoveredEdgeExists().w == -1) { // 没有未覆盖的点
				Vertex *u = getVertexWithHighestDScoreFromC(elapsedTime);
				removeFromC(u->id);
				vertices[u->id - 1].time = elapsedTime;
				elapsedTime++;
				continue;
			}
			Vertex *u = getVertexWithHighestDScoreFromC(elapsedTime); 
			removeFromC(u->id);
			vertices[u->id - 1].time = elapsedTime;
			u->confChange = 0;
			for (Edge e : u->edges) {
				vertices[e.id - 1].confChange = 1;
			}
			Edge e = uncoveredEdgeExists();
			Vertex *v = chooseOneVertex(e, elapsedTime);
			addToC(v->id);
			vertices[v->id - 1].time = elapsedTime;
			for (Edge e1 : v->edges) {
				vertices[e1.id - 1].confChange = 1;
			}
			weightUpdate();
			updateMean();
			if (mean >= gamma)
				updateWeight();
			elapsedTime++;
		}
		for (int i = 1; i <= vertices.size(); i++)
			if(vertices[i].isInC)
				coverHeu.insert(i);
	}

private:
	void computeHeuVC() { // 根据启发式算法导出第一个覆盖
		for (int each : coverHeu)
			addToC(each);
	}

	// unused
	void computeGreedyVC() { // 贪心取得一个点覆盖
		Edge e;
		while ((e = uncoveredEdgeExists()).w != -1) {
			if (!(e.covered)) {
				addToC(e.id);
			}
		}
	}

	Edge uncoveredEdgeExists() { // 如果所有边都被覆盖，返回一个空边；如果有未被覆盖的边，随机返回其中一个
		vector<Edge> edges = vector<Edge>();
		for (Vertex vertex : vertices) {
			for (Edge e : vertex.edges) { 
				if (!e.covered) {
					edges.push_back(e);
				}
			}
		}
		if (edges.empty())
			return Edge(); // 空边

		int rand = int(random(0, edges.size()));

		return edges[rand];
	}

	void setEdge(int n, bool v) { // 把节点n的所有边设置成v
		vertices[n - 1].isInC = true; 
		for (Edge &e : vertices[n - 1].edges) {
			e.covered = v;
			for (Edge &e1 : vertices[e.id - 1].edges) {
				if (e1.id == n) {
					e1.covered = v;
					break;
				}
			}
		}
	}

	void addToC(int n) { // 把节点n加入覆盖
		setEdge(n, true);
	}

	void removeFromC(int n) { // 把节点n移出覆盖
		setEdge(n, false);
		vertices[n - 1].isInC = false;
		for (Edge e : vertices[n - 1].edges) {
			if (vertices[e.id - 1].isInC) // 如果n的邻居中有还在覆盖内的
				addToC(e.id); // 把n放回覆盖
		}
	}

	void updateWeight() { // 每条边的权值衰减
		for (Vertex &vertex : vertices) {
			for (Edge &e : vertex.edges) {
				e.w = (int)(rho * e.w);
			}
		}
	}

	void updateMean() {
		double sum = 0, i = 0;
		for (Vertex vertex : vertices) {
			for (Edge e : vertex.edges) {
				sum += e.w;
				i++;
			}
		}
		mean = sum / i;
	}

	void weightUpdate() {
		for (Vertex &vertex : vertices) {
			for (Edge &e : vertex.edges) {
				if (!e.covered) {
					e.w++;
				}
			}
		}
	}

	Vertex* chooseOneVertex(Edge e, int k) { // 选一个顶点
		updateDScores();

		Vertex* res = NULL;
		if (vertices[e.from - 1].confChange == 1) {
			if (vertices[e.id - 1].confChange == 1) {
				if (vertices[e.id - 1].dscore > vertices[e.from - 1].dscore) {
					res = &vertices[e.id - 1];
				}
				else if (vertices[e.id - 1].dscore == vertices[e.from - 1].dscore) {
					if ((k - vertices[e.id - 1].time) > (k - vertices[e.from - 1].time))
						res = &vertices[e.id - 1];
					else
						res = &vertices[e.from - 1];
				}
				else
					res = &vertices[e.from - 1];
			}
			else {
				res = &vertices[e.from - 1];
			}
		}
		else if (vertices[e.id - 1].confChange == 1) {
			res = &vertices[e.id - 1];
		}
		return res;
	}

	Vertex* getVertexWithHighestDScoreFromC(int k) { // 从目前覆盖中找出有最高dscore的顶点
		updateDScores();
		Vertex *high_d = NULL;
		for (Vertex &vertex : vertices) {
			if (vertex.isInC) {
				if (high_d == NULL) {
					high_d = &vertex;
					continue;
				}
				if (vertex.dscore > high_d->dscore) {
					high_d = &vertex;
				}
				else if (vertex.dscore == high_d->dscore) { // 打平时要更老的那个
					if ((k - vertex.time) > (k - high_d->time))
						high_d = &vertex;
				}
			}
		}
		return high_d;
	}

	void updateDScores() { // 已知本次增/删的点u，更新每个点的dscore
		for (Vertex &vertex : vertices) {
			vertex.dscore = getDScore(vertex);
		}
	}

	int getDScore(Vertex v) { 
		int dscore = 0;
		for (Edge edge : v.edges)
		{
			if (!vertices[edge.id - 1].isInC)
				dscore += edge.w;
		}
		if (v.isInC)
			return -dscore;
		return dscore;
	}
};

class Converter
{ // 取得补图的边集
public:
	vector<vector<bool>> adjMat;	// 邻接矩阵
	vector<vector<bool>> cmpAdjMat; // 补图的邻接矩阵
	int V, E;

	Converter(char* filepath)
	{
		freopen(filepath, "r", stdin);
		scanf("p edge %d %d\n", &V, &E);
		adjMat = vector<vector<bool>>(V);
		cmpAdjMat = vector<vector<bool>>(V);
		for (int i = 0; i < V; i++)
		{
			adjMat[i] = vector<bool>(V, false);
			cmpAdjMat[i] = vector<bool>(V, true);
		}
		int s, t;
		for (int i = 0; i < E; i++)
		{
			scanf("e %d %d\n", &s, &t);
			cmpAdjMat[s - 1][t - 1] = false; cmpAdjMat[t - 1][s - 1] = false;
			adjMat[s - 1][t - 1] = true; adjMat[t - 1][s - 1] = true;
		}

		for (int i = 0; i < V; i++)
			cmpAdjMat[i][i] = false;
	}

	vector<vector<int>> ConvertedEdgeList()
	{
		vector<vector<int>> convertedEdgeList = vector<vector<int>>(V);
		for (int i = 0; i < V; i++)
		{
			for (int j = 0; j < V; j++)
			{
				if (cmpAdjMat[i][j])
					convertedEdgeList[i].push_back(j + 1);
			}
		}
		return convertedEdgeList;
	}
};

class MaxCliqueHeu
{
public:
	int maxsize; //maxsize 最大团点数
	vector<int> d; //d 度数 
	vector<vector<bool>> a;
	unordered_set<int> maxCliqueHeu; // 启发式算法找到的极大团(基数为0)

	MaxCliqueHeu() {}

	void CliqueHeu(unordered_set<int> U, int size, unordered_set<int> S)
	{
		if (U.size() + size <= maxsize) return;
		if (U.empty())
		{
			if (size > maxsize)
			{
				maxsize = size;
				maxCliqueHeu = S;
			}
			return;
		}
		unordered_set<int>::iterator it;
		int u = 0, maxd = 0;
		for (it = U.begin(); it != U.end(); it++)
			if (d[*it] > maxd)
			{
				u = *it;
				maxd = d[*it];
			}

		// best answer
		U.erase(u);
		S.insert(u);
		unordered_set<int>::iterator is;
		unordered_set<int> U_N;
		for (is = U.begin(); is != U.end(); is++)
			if ((a[u][*is])&(d[*is] > maxsize))
				U_N.insert(*is);
		CliqueHeu(U_N, size + 1, S);
	}

	MaxCliqueHeu(vector<vector<bool>> original)
	{
		this->a = vector<vector<bool>>(original);
		maxsize = 0;
		d = vector<int>(original.size(), 0);
		for (int i = 0; i < d.size(); i++)
			for (int j = 0; j < d.size(); j++)
				if (a[i][j]) d[i]++;
		
		for (int i = 1; i <= original.size(); i++)
			if (d[i] >= maxsize)
			{
				unordered_set<int> U;
				for (int j = 1; j <= original.size(); j++)
					if ((a[i][j])&(d[j] >= maxsize))
						U.insert(j);
				unordered_set<int> S;
				S.insert(i);
				CliqueHeu(U, 1, S);
			}
		printf("HeuCount: %d\n", maxsize);
	}

	unordered_set<int> complementaryCover() { // 基于这个极大图找到补图中的一个点覆盖(基数为1)
		unordered_set<int> cplCover;
		for (int i = 0; i < a.size(); i++)
		{
			auto it = maxCliqueHeu.find(i);
			if (it == maxCliqueHeu.end())
				cplCover.insert(i + 1);
		}
		return cplCover;
	}
};

int main()
{
	srand(unsigned(time(0)));
	char* filepath = "frb30-15-1.clq";
	Converter converter = Converter(filepath);
	MaxCliqueHeu MCH = MaxCliqueHeu(converter.adjMat);

	Graph graph = Graph(converter.ConvertedEdgeList());
	graph.startTime = clock();
	graph.cutOff = 100000;
	graph.coverHeu = MCH.complementaryCover();
	graph.computeNuMVC();

	printf("The maximum clique found: ");
	for (int i = 1; i <= converter.cmpAdjMat.size(); i++)
		if (graph.coverHeu.find(i) == graph.coverHeu.end())
			printf("%d ", i);
	printf("\n");
}
