#include <QApplication>
#include <QPushButton>
#include <QWidget>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QWidget window;
    window.setFixedSize(400, 300);

    QPushButton button("Hello, World!", &window);
    button.setGeometry(100, 100, 200, 50);

    window.show();

    return app.exec();
}