// ConsoleApplication1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <vector>
#include <string>
#include <climits>

using namespace std;

class Coordinate {
public:
	double X, Y;
	Coordinate();
	Coordinate(double, double);
	void move(double, double);
};
class Vector {
public:
	Coordinate head, tail;
	Vector(Coordinate, Coordinate);
	double vecAngle();
	double distance();
	double getheading();
	void rotate(double);
private:
	const double fullcirclerad = 2 * 3.141592653589;
};
class Polygon {
public:
	Polygon(int, Coordinate);
	Polygon(double, Coordinate, int);
	Polygon(vector<Coordinate>);
	void rotate(double angle);
	double difference(Polygon);
	double getheading();
	Vector box();
	Polygon bestpoly(double);
private:
	int n;
	Coordinate center;
	vector<Coordinate> positions;
	static const double accdeg;
	static const double acccen;
	static const double adjustment;
	static const double fullcircledeg;
};
const double Polygon::accdeg = .5;
const double Polygon::acccen = 0.000001;
const double Polygon::adjustment = 4.0;
const double Polygon::fullcircledeg = 360;

double change(double angle, bool iftodeg);
bool isDouble(string str);
void runNgps(int n, double distanceRadius, vector<Coordinate> points, string filename, string time);

int main(int argc, char *argv[]) {
	// check argc
	vector<Coordinate> points;
	
	//char* temparg[] = { "1","2","3","4","5","6","7","8","testfile.txt" };
	ofstream fout((string)argv[9], std::ios::app);

	//fout << argv[1] << ' ' << argv[2] << ' ' << argv[3] << ' ' << argv[4] << endl;
	if (argc != 11) {
		fout << "ARGC NOT 11\n";
		return -1;
	}
	//bool ifViable = true;
	for (int i = 1; i < 8; i += 2) {
		//ifViable = ifViable && isDouble((string)argv[i]) && isDouble((string)argv[i + 1]);
		double x = stod((string)argv[i]), y = stod((string)argv[i + 1]);
		//		double x = stod((string)temparg[i]), y = stod((string)temparg[i + 1]);
		Coordinate point(x, y);
		points.push_back(point);
	}
	/*if (!ifViable) {
		fout << "ERROR MESSAGE - rip DR\n";
		return -1;
	}
	else {*/
		double distanceRadius = .00001182, errorRadius = 2.5;
		int n = 4;
		runNgps(n, distanceRadius, points, (string)argv[9], (string)argv[10]);
		return 0;
	//}
}

Coordinate::Coordinate() {
	X = 0;
	Y = 0;
}
Coordinate::Coordinate(double x, double y) {
	X = x;
	Y = y;
}
void Coordinate::move(double deltax, double deltay) {
	X += deltax;
	Y += deltay;
}

Vector::Vector(Coordinate headi, Coordinate taili) {
	head = headi;
	tail = taili;
}
double Vector::vecAngle() {
	return atan2(head.Y - tail.Y, head.X - tail.X);
}
double Vector::distance() {
	double dist = (head.X - tail.X) * (head.X - tail.X);
	dist += (head.Y - tail.Y) * (head.Y - tail.Y);
	return dist;
}
double Vector::getheading() {
	double angRadians = vecAngle();
	if (angRadians < 0) angRadians += fullcirclerad;
	return change(angRadians, true);
}
void Vector::rotate(double angle) {
	angle = change(angle, false);
	Coordinate rot = head;
	rot.move(-tail.X, -tail.Y);
	double newx = rot.X * cos(angle) - rot.Y * sin(angle);
	double newy = rot.X * sin(angle) + rot.Y * cos(angle);
	head = Coordinate(newx, newy);
	head.move(tail.X, tail.Y);
}

Polygon::Polygon(int input, Coordinate centeri) {
	positions = vector<Coordinate>(input);
	n = input;
	center = centeri;
}
Polygon::Polygon(double distanceRadius, Coordinate centeri, int ni) {
	center = centeri;
	n = ni;
	positions = vector<Coordinate>(ni);
	const double fullcircle = 360;
	Vector curr(Coordinate(center.X, center.Y + distanceRadius), center); // top
	positions[0] = curr.head;
	for (int i = 1; i < n; i++) {
		curr.rotate(fullcircle / n);
		positions[i] = curr.head;
	}
}
Polygon::Polygon(vector<Coordinate> points) {
	center = points[0];
	n = points.size();
	positions = points;
}
void Polygon::rotate(double angle) {
	vector <Coordinate> newpos(n);
	for (int i = 0; i < n; i++) {
		Vector vec(positions[i], center);
		vec.rotate(angle);
		newpos[i] = vec.head;
	}
	positions = newpos;
}
double Polygon::difference(Polygon s2) {
	double diff = 0;
	for (int i = 0; i < n; i++) {
		Vector vec(positions[i], s2.positions[i]);
		diff += vec.distance();
	}
	return diff;
}
double Polygon::getheading() {
	Vector north = Vector(positions[0], center);
	return north.getheading();
}
Vector Polygon::box() {
	double farleft = INT_MAX, farbot = INT_MAX; // could be LLONG_MAX, who cares
	double farright = INT_MIN, fartop = INT_MIN;
	for (int i = 0; i < n; i++) {
		if (positions[i].X < farleft) farleft = positions[i].X;
		if (positions[i].X > farright) farright = positions[i].X;
		if (positions[i].Y < farbot) farbot = positions[i].Y;
		if (positions[i].Y > fartop) fartop = positions[i].Y;
	}
	double xdist = farright - farleft, ydist = fartop - farbot;

	farleft += xdist / adjustment; // narrow algorithm's search space
	farbot += ydist / adjustment;
	farright -= xdist / adjustment;
	fartop -= ydist / adjustment;

	Coordinate head(farright, fartop);
	Coordinate tail(farleft, farbot);
	return Vector(head, tail);
}
Polygon Polygon::bestpoly(double distanceRadius) {
	Polygon bestsim = *this;
	Polygon currsim = *this;
	double minerror = 10000;
	Vector boxx = box();
	for (double x = boxx.tail.X; x < boxx.head.X; x += acccen) {
		for (double y = boxx.tail.Y; y < boxx.head.Y; y += acccen) {
			//std::cout << x << " " << y << '\n';
			Coordinate center(x, y);
			currsim = Polygon(distanceRadius, center, n);
			//currsim.rotate (-fullcircle / (2*n));
			for (int i = 0; i < fullcircledeg / (accdeg); i++) {
				//cout << difference(currsim) << endl;
				if (difference(currsim) < minerror) {
					minerror = difference(currsim);
					bestsim = currsim;
				}
				currsim.rotate(accdeg);
			}
		}
	}
	return bestsim;
}

double change(double angle, bool iftodeg) {
	const double multiplier = 180 / 3.141592653;
	if (iftodeg) return angle * multiplier;
	else return angle / multiplier;
}

bool isDouble(string str) {
	int len = str.length();
	for (int i = 0; i < len; i++) {
		char c = str[i];
		if (((c - '0' < 0) || (c - '0' > 9)) && c != '.') return false;
	}
	return true;
}

void runNgps(int n, double distanceRadius, vector<Coordinate> points, string filename, string time) {
	//fout << fixed << setprecision(0);
	ofstream fout(filename, std::ios::app);
	double x, y, sumdist = 0;
	string unneeded;

	Vector vert(points[0], points[1]);
	Vector hori(points[2], points[3]);

	distanceRadius = (sqrt(vert.distance()) + sqrt(hori.distance())) / 4;
	Polygon newpoly(points);
	Polygon bestpol = newpoly.bestpoly(distanceRadius);
	double heading = bestpol.getheading();
	heading = 90 - heading;
	if (heading < 0) heading += 360;
	fout << time << ',' << heading << ',';

	double heading1 = (vert.getheading() + hori.getheading() + 90) / 2;
	heading1 = 90 - heading1;
	if (heading1 < 0) heading1 += 360;
	fout << time << ',' << heading1 << "\n";
}
