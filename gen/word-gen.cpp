#include <bits/stdc++.h>
using namespace std;
using Shapes = array<array<array<int, 4>, 5>, 26>;

constexpr Shapes initShapes() {
    constexpr Shapes shapes = {{
        {{ // a
            {0,1,0,0},
            {1,0,1,0},
            {1,1,1,0},
            {1,0,1,0},
            {1,0,1,0}
        }},

        {{ // b
            {1,1,1,0},
            {1,0,1,0},
            {1,1,1,0},
            {1,0,1,0},
            {1,1,1,0}
        }},

        {{ // c
            {1,1,1,0},
            {1,0,0,0},
            {1,0,0,0},
            {1,0,0,0},
            {1,1,1,0}
        }},

        {{ // d
            {1,1,0,0},
            {1,0,1,0},
            {1,0,1,0},
            {1,0,1,0},
            {1,1,0,0}
        }},

        {{ // e
            {1,1,1,0},
            {1,0,0,0},
            {1,1,0,0},
            {1,0,0,0},
            {1,1,1,0}
        }},

        {{ // f
            {1,1,1,0},
            {1,0,0,0},
            {1,1,0,0},
            {1,0,0,0},
            {1,0,0,0}
        }},

        {{ // g
            {1,1,1,0},
            {1,0,0,0},
            {1,0,1,0},
            {1,0,1,0},
            {1,1,1,0}
        }},

        {{ // h
            {1,0,1,0},
            {1,0,1,0},
            {1,1,1,0},
            {1,0,1,0},
            {1,0,1,0}
        }},

        {{ // i
            {1,1,1,0},
            {0,1,0,0},
            {0,1,0,0},
            {0,1,0,0},
            {1,1,1,0}
        }},

        {{ // j
            {1,1,1,0},
            {0,1,0,0},
            {0,1,0,0},
            {0,1,0,0},
            {1,1,0,0}
        }},

        {{ // k
            {1,0,1,0},
            {1,0,1,0},
            {1,1,0,0},
            {1,0,1,0},
            {1,0,1,0}
        }},

        {{ // l
            {1,0,0,0},
            {1,0,0,0},
            {1,0,0,0},
            {1,0,0,0},
            {1,1,1,0}
        }},

        {{ // m
            {1,0,1,0},
            {1,1,1,0},
            {1,1,1,0},
            {1,1,1,0},
            {1,0,1,0}
        }},

        {{ // n
            {1,0,1,0},
            {1,1,1,0},
            {1,0,1,0},
            {1,0,1,0},
            {1,0,1,0}
        }},

        {{ // o
            {0,1,0,0},
            {1,0,1,0},
            {1,0,1,0},
            {1,0,1,0},
            {0,1,0,0}
        }},

        {{ // p
            {1,1,1,0},
            {1,0,1,0},
            {1,1,1,0},
            {1,0,0,0},
            {1,0,0,0}
        }},

        {{ // q
            {0,1,0,0},
            {1,0,1,0},
            {1,0,1,0},
            {0,1,0,0},
            {0,0,1,0}
        }},

        {{ // r
            {1,1,1,0},
            {1,0,1,0},
            {1,1,0,0},
            {1,0,1,0},
            {1,0,1,0}
        }},
        

        {{ // s
            {1,1,1,0},
            {1,0,0,0},
            {1,1,1,0},
            {0,0,1,0},
            {1,1,1,0}
        }},

        {{ // t
            {1,1,1,0},
            {0,1,0,0},
            {0,1,0,0},
            {0,1,0,0},
            {0,1,0,0}
        }},

        {{ // u
            {1,0,1,0},
            {1,0,1,0},
            {1,0,1,0},
            {1,0,1,0},
            {1,1,1,0}
        }},

        {{ // v
            {1,0,1,0},
            {1,0,1,0},
            {1,0,1,0},
            {1,0,1,0},
            {0,1,0,0}
        }},

        {{ // w
            {1,0,1,0},
            {1,0,1,0},
            {1,1,1,0},
            {1,1,1,0},
            {1,0,1,0}
        }},

        {{ // x
            {1,0,1,0},
            {0,1,0,0},
            {0,1,0,0},
            {1,0,1,0},
            {1,0,1,0}
        }},

        {{ // y
            {1,0,1,0},
            {1,0,1,0},
            {0,1,0,0},
            {0,1,0,0},
            {0,1,0,0}
        }},

        {{ // z
            {1,1,1,0},
            {0,0,1,0},
            {0,1,0,0},
            {1,0,0,0},
            {1,1,1,0}
        }},
    }};

    return shapes;
}


enum Letters {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z};
constexpr Shapes shapes = initShapes();




vector<pair<int, int>> Encode(const vector<string> & text) {
    vector<pair<int, int>> encoding;
    
    int n = 0;
    for(const auto & s : text) {
        n = max<int>(n, s.length());
    }
    n = 2 + 4*n;
    n = max<int>(n, 6*text.size()+2);

    int f = 0;
    for(const auto & s : text) {
        for(const auto c : s) {
            for(const auto & row : shapes[c-'a']) {
                f += accumulate(row.begin(), row.end(), 0);
            }
        }
    }

    int x = 2, y;
    for(const auto & s : text) {
        y = 2;
        for(const auto c : s) {
            auto shape = shapes[c-'a'];
            for(int i=0; i<5; ++i) {
                for(int j=0; j<4; ++j) {
                    if(shape[i][j]) {
                        encoding.emplace_back(x+i, y+j);
                    }
                }
            }

            y += 4;
        }

        x += 6;
    }

    encoding.emplace_back(n, f);
    return encoding;
}


void PrintAsp(vector<pair<int, int>> & encoding) {
    const auto [n, f] = encoding.back();
    encoding.pop_back();

    cout << "#const n = " << n << ".\n";
    cout << "#const f = " << f << ".\n";
    cout << "#const s = 100.\n";
    cout << "#const r = 100.\n";
    cout << "#const l = 100.\n";

    for(const auto & [x, y] : encoding) {
        cout << "val(" << x << ", " << y << ", xxx).\n";
    }
}



int main()
{
    auto encoding = Encode({"giacomo", "ettore", "farlocco"});

    PrintAsp(encoding);
}