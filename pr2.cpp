// Адам Голота, 232/1
// Варіант 31 – Діалоговий режим: Сервер не закриває з'єднання одразу, а дозволяє клієнту надіслати 3 повідомлення перед викликом close(clientSocket).
#include <iostream>     // Прикладний рівень: виведення логів у консоль
#include <sys/socket.h> // Транспортний рівень: доступ до функцій сокетів
#include <netinet/in.h> // Мережевий рівень: структури для IP-адрес
#include <unistd.h>      // Системні виклики (read/close)
#include <cstring>     // Робота з масивами символів

int main() {
    // Створення сокета: AF_INET (IPv4 - Мережевий рівень), SOCK_STREAM (TCP - Транспортний рівень)
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0) {
        std::cerr << "Помилка створення сокета" << std::endl;
        return -1;
    }

    // Налаштування структури адреси сервера (Мережевий + Транспортний рівні)
    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;           // Протокол IPv4
    serverAddress.sin_addr.s_addr = INADDR_ANY;   // Слухати всі мережеві інтерфейси хоста
    serverAddress.sin_port = htons(8080);         // Порт додатка (Транспортний рівень)

    // Прив’язка сокета (bind): резервування порту 8080 в ОС для нашого додатка
    if (bind(serverSocket, (sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        std::cerr << "Помилка прив’язки сокета" << std::endl;
        return -1;
    }

    // Очікування (listen): сервер готовий приймати запити на встановлення TCP-з'єднання
    if (listen(serverSocket, 3) < 0) {
        std::cerr << "Помилка прослуховування" << std::endl;
        return -1;
    }

    std::cout << "Сервер очікує на підключення клієнтів..." << std::endl;

    // Прийом з’єднання (accept): завершення TCP 3-way handshake та створення окремого сокета для сесії
    int clientSocket;
    sockaddr_in clientAddress;
    socklen_t clientLength = sizeof(clientAddress);
    clientSocket = accept(serverSocket, (sockaddr*)&clientAddress, &clientLength);
    
    if (clientSocket < 0) {
        std::cerr << "Помилка приймання клієнта" << std::endl;
        return -1;
    }

    // --- ПОЧАТОК ДІАЛОГОВОГО РЕЖИМУ (Прикладний рівень) ---
    for (int i = 0; i < 3; ++i) {
        char buffer[1024] = {0};
        
        // Читання даних з буфера прийому TCP-стеку
        int bytesRead = read(clientSocket, buffer, 1024);
        if (bytesRead > 0) {
            std::cout << "[" << i + 1 << "] Отримано: " << buffer << std::endl;
            
            // Формування відповіді рівня додатка
            std::string responseMsg = "Server received msg " + std::to_string(i + 1);
            const char* response = responseMsg.c_str();
            
            // Відправка відповіді клієнту через встановлений транспортний канал
            send(clientSocket, response, strlen(response), 0);
        }
    }
    // --- КІНЕЦЬ ДІАЛОГОВОГО РЕЖИМУ ---

    // Закриття сесії клієнта: ініціалізація процедури завершення TCP-з'єднання (FIN пакет)
    close(clientSocket);
    // Закриття слухаючого сокета: звільнення порту 8080
    close(serverSocket);

    return 0;
}