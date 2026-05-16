// Адам Голота, 232/1
// Варіант 31 – Додайте коментар до кожного рядка коду, пояснюючи його роль у моделі TCP/IP.
#include <iostream>     // Стандартне введення-виведення для логування помилок
#include <sys/socket.h> // Надає функції для роботи з сокетами (Транспортний рівень)
#include <arpa/inet.h>  // Функції для роботи з IP-адресами (Мережевий рівень)
#include <unistd.h>      // Для системного виклику close()
#include <cstring>     // Для обчислення довжини рядка повідомлення

int main() {
    // Створення кінцевої точки зв'язку. AF_INET вказує на IPv4 (Мережевий рівень), 
    // SOCK_STREAM визначає протокол TCP (Транспортний рівень).
    int clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    
    // Перевірка, чи операційна система змогла виділити дескриптор сокета
    if (clientSocket < 0) {
        std::cerr << "Помилка створення сокета" << std::endl;
        return -1;
    }

    // Оголошення структури для зберігання адреси вузла призначення (Мережевий та Транспортний рівні)
    sockaddr_in serverAddress;

    // Визначає сімейство протоколів IPv4 для адресації в мережі
    serverAddress.sin_family = AF_INET; 
    
    // Встановлює порт (8080). htons конвертує число у формат Big-Endian, необхідний для TCP/IP
    serverAddress.sin_port = htons(8080); 

    // Конвертація рядка IP-адреси у двійковий формат, який розуміє Мережевий рівень (IP)
    if (inet_pton(AF_INET, "192.168.1.1", &serverAddress.sin_addr) <= 0) {
        std::cerr << "Невірна IP-адреса або адреса не підтримується" << std::endl;
        return -1;
    }

    // Ініціалізація "трьохстороннього рукостискання" (3-way handshake) протоколу TCP 
    // для встановлення логічного зв'язку між клієнтом та сервером.
    if (connect(clientSocket, (sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        std::cerr << "Не вдалося встановити з’єднання" << std::endl;
        return -1;
    }

    // Дані рівня додатків (Application Layer)
    const char *message = "Hello Server";
    
    // Інкапсуляція даних у сегмент TCP та передача їх вниз по стеку для відправки
    send(clientSocket, message, strlen(message), 0);

    // Розірвання TCP-з'єднання та звільнення ресурсів операційної системи
    close(clientSocket);

    return 0;
}