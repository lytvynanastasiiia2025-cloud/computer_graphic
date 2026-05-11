#include <windows.h>
#include <fstream>

const int CENTER_X = 200;
const int CENTER_Y = 200;
const int SCALE = 8;

void bresenham_line(HDC hdc, int x0, int y0, int x1, int y1) {
    int dx = abs(x1 - x0);  // vector displacement
    int dy = abs(y1 - y0);

    int sx = (x0 < x1) ? 1 : -1;  // step in x direction
    int sy = (y0 < y1) ? 1 : -1;

    int err = dx - dy;

    while (true) {
        SetPixel(hdc, x0, y0, RGB(255, 255, 255));  // draw one pixel

        if (x0 == x1 && y0 == y1) break;

        int e2 = 2 * err;
        if (e2 > -dy) { err -= dy; x0 += sx; }
        if (e2 <  dx) { err += dx; y0 += sy; }
    }
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);

            // Fill background black
            RECT rect;
            GetClientRect(hwnd, &rect);
            FillRect(hdc, &rect, (HBRUSH)GetStockObject(BLACK_BRUSH));

            // Direction vectors
            int vectors[][2] = {
                { 20,  10}, { 10,  20}, {-10,  20}, {-20,  10},
                {-20, -10}, {-10, -20}, { 10, -20}, { 20, -10}
            };

            // Draw all rays from center
            for (int i = 0; i < 8; i++) {
                int target_x = CENTER_X + vectors[i][0] * SCALE;
                int target_y = CENTER_Y + vectors[i][1] * SCALE;
                bresenham_line(hdc, CENTER_X, CENTER_Y, target_x, target_y);
            }

            EndPaint(hwnd, &ps);
            break;
        }
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int main() {
    HINSTANCE hInstance = GetModuleHandle(NULL);
    
    WNDCLASS wc = {};
    wc.lpfnWndProc   = WndProc;
    wc.hInstance     = hInstance;
    wc.lpszClassName = "BresenhamWindow";
    wc.hbrBackground = (HBRUSH)GetStockObject(BLACK_BRUSH);
    RegisterClass(&wc);

    HWND hwnd = CreateWindow(
        "BresenhamWindow", "Bresenham Algorithm",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 420, 440,
        NULL, NULL, hInstance, NULL
    );

    ShowWindow(hwnd, SW_SHOW);
    UpdateWindow(hwnd);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}