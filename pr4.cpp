// Адам Голота, 232/1
// Варіант 31 – Чат-бот: Сервер аналізує ключові слова ("привіт", "бувай") і надсилає відповідні реакції.

#include <iostream>
#include <sys/socket.h> // Транспортний рівень: сокети
#include <netinet/in.h> // Мережевий рівень: IP-структури
#include <unistd.h>     // Системні виклики (read/close)
#include <cstring>
#include <string>       // Для зручного аналізу тексту на прикладному рівні

int main() {
    // Створення сокета (TCP/IPv4)
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0) {
        std::cerr << "Помилка створення сокета" << std::endl;
        return -1;
    }

    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = INADDR_ANY; // Слухати всі інтерфейси
    serverAddress.sin_port = htons(8080);      // Порт додатку

    // Прив’язка сокета до порту
    if (bind(serverSocket, (sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        std::cerr << "Помилка прив’язки" << std::endl;
        return -1;
    }

    // Очікування з'єднання
    listen(serverSocket, 3);
    std::cout << "Чат-бот запущений і чекає на повідомлення..." << std::endl;

    int clientSocket;
    sockaddr_in clientAddress;
    socklen_t clientLength = sizeof(clientAddress);
    clientSocket = accept(serverSocket, (sockaddr*)&clientAddress, &clientLength);

    // --- ЛОГІКА ЧАТ-БОТА (Прикладний рівень) ---
    char buffer[1024] = {0};
    // Отримання даних з транспортного рівня
    int bytesRead = read(clientSocket, buffer, 1024);
    
    if (bytesRead > 0) {
        std::string receivedText(buffer);
        std::cout << "Клієнт написав: " << receivedText << std::endl;

        std::string response;
        // Аналіз ключових слів (Прикладний рівень)
        if (receivedText.find("привіт") != std::string::npos || receivedText.find("Привіт") != std::string::npos) {
            response = "Бот: Вітаю! Чим можу допомогти?";
        } 
        else if (receivedText.find("бувай") != std::string::npos || receivedText.find("Бувай") != std::string::npos) {
            response = "Бот: До зустрічі! Гарного дня!";
        } 
        else {
            response = "Бот: Я розумію лише 'привіт' або 'бувай'.";
        }

        // Надсилання сформованої відповіді назад по стеку TCP/IP
        send(clientSocket, response.c_str(), response.length(), 0);
    }

    // Закриття з'єднання
    close(clientSocket);
    close(serverSocket);
    return 0;
}
