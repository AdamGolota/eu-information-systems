// Адам Голота, 232/1
// Варіант 31 – Стрес-тест: Надішліть 1000 коротких повідомлень максимально швидко і виміряйте час виконання.

#include <iostream>
#include <sys/socket.h> // Транспортний рівень: робота з TCP-сокетами
#include <arpa/inet.h>  // Мережевий рівень: конвертація IP-адрес
#include <unistd.h>     // Системні виклики: close()
#include <cstring>
#include <chrono>       // Прикладний рівень: вимірювання продуктивності

int main() {
    // Створення сокета (Транспортний рівень, протокол TCP)
    int clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket < 0) {
        std::cerr << "Помилка створення сокета" << std::endl;
        return -1;
    }

    // Налаштування адреси сервера (Мережевий рівень)
    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(8080); // Порт (Транспортний рівень)

    if (inet_pton(AF_INET, "127.0.0.1", &serverAddress.sin_addr) <= 0) {
        std::cerr << "Невірна адреса" << std::endl;
        return -1;
    }

    // Встановлення з'єднання (TCP 3-way handshake)
    if (connect(clientSocket, (sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        std::cerr << "З'єднання не вдалося" << std::endl;
        return -1;
    }

    // --- ПОЧАТОК СТРЕС-ТЕСТУ (Прикладний рівень) ---
    const char *message = "Test";
    int iterations = 1000;

    // Фіксація часу початку тесту
    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < iterations; ++i) {
        // Швидка передача даних у буфер сокета. 
        // На транспортному рівні TCP може об'єднувати ці повідомлення (алгоритм Нагла).
        send(clientSocket, message, strlen(message), 0);
    }

    // Фіксація часу завершення
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> diff = end - start;

    std::cout << "Стрес-тест завершено." << std::endl;
    std::cout << "Надіслано " << iterations << " повідомлень за " << diff.count() << " секунд." << std::endl;
    // --- КІНЕЦЬ СТРЕС-ТЕСТУ ---

    // Закриття з'єднання (Транспортний рівень)
    close(clientSocket);
    return 0;
}
