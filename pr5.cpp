// Адам Голота, 232/1
// Варіант 31 – Тестування навантаження: Написати скрипт для створення 1000 одночасних підключень до сервера.

#include <boost/asio.hpp>
#include <iostream>
#include <vector>
#include <memory>

using boost::asio::ip::tcp;

// Клас одного клієнтського підключення (Сесія прикладного рівня)
class Connection : public std::enable_shared_from_this<Connection> {
public:
    Connection(boost::asio::io_context& ioContext) 
        : socket_(ioContext) {} // Ініціалізація структури сокета в ядрі через Asio

    void start(const tcp::endpoint& endpoint) {
        // Запуск асинхронного встановлення TCP-з'єднання (3-way handshake).
        // Функція не блокує потік, а одразу повертає керування.
        auto self(shared_from_this());
        socket_.async_connect(endpoint,
            [self](const boost::system::error_code& error) {
                if (!error) {
                    // З'єднання перейшло у стан ESTABLISHED на Транспортному рівні.
                    // Утримуємо його відкритим, нічого не закриваючи.
                } else {
                    std::cerr << "Помилка підключення: " << error.message() << std::endl;
                }
            });
    }

private:
    tcp::socket socket_; // Об'єкт сокета (Транспортний рівень)
};

int main() {
    try {
        // Менеджер подій ядра, що координує неблокуючі виклики
        boost::asio::io_context ioContext;

        // Мережевий рівень: Визначення цільової IPv4 адреси та порту сервера (127.0.0.1:8080)
        tcp::endpoint endpoint(boost::asio::ip::make_address("127.0.0.1"), 8080);

        // Вектор для зберігання вказівників на сесії, щоб вони не знищувалися в пам'яті
        std::vector<std::shared_ptr<Connection>> connections;
        int totalConnections = 1000;

        std::cout << "Ініціалізація " << totalConnections << " асинхронних підключень..." << std::endl;

        // Генерація 1000 підключень
        for (int i = 0; i < totalConnections; ++i) {
            auto conn = std::make_shared<Connection>(ioContext);
            connections.push_back(conn);
            conn->start(endpoint); // Реєстрація запиту на підключення в черзі подій ОС
        }

        // Прикладний рівень передає контроль ядру:
        // Цей виклик запускає цикл, який чекає на завершення TCP-рукостискань для всіх 1000 сокетів
        ioContext.run();

        std::cout << "Усі події оброблені." << std::endl;

    } catch (std::exception& e) {
        std::cerr << "Виключення: " << e.what() << std::endl;
    }

    return 0;
}
