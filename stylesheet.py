def get_stylesheet():
    return """
    QMainWindow {
        background-color: #2c3e50;
    }
    QLabel {
        font-size: 14px;
        color: white;
    }
    QLineEdit {
        background-color: white;
        color: black;
        padding: 5px;
        border-radius: 5px;
        font-size: 14px;
    }
    QPushButton {
        background-color: #3498db;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
    QTableWidget {
        background-color: white;
        font-size: 14px;
    }
    QHeaderView::section {
        background-color: #3498db;
        color: white;
        padding: 5px;
        border: none;
        font-size: 14px;
    }
    QStatusBar {
        background-color: #34495e;
        color: white;
    }
    QMenuBar {
        background-color: #34495e;
        color: white;
    }
    QMenuBar::item {
        background-color: #34495e;
        color: white;
    }
    QMenuBar::item:selected {
        background-color: #2c3e50;
    }
    QMenu {
        background-color: #34495e;
        color: white;
    }
    QMenu::item {
        background-color: #34495e;
        color: white;
    }
    QMenu::item:selected {
        background-color: #2c3e50;
    }
    """
