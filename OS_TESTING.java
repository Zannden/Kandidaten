import javax.microedition.io.Connector;
import javax.microedition.io.StreamConnection;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Scanner;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class OS_TESTING {
    private static final String url = "btspp://B827EB418F6D:1;authenticate=false;encrypt=false;master=false";
    private static ExecutorService threadPool = Executors.newFixedThreadPool(2);

    public static void main(String[] args) {
        StreamConnection conn = null;

        try {
            conn = (StreamConnection) Connector.open(url);
            OutputStream out = conn.openOutputStream();
            InputStream in = conn.openInputStream();

            // Wait for the connection to be established
            System.out.println("Connection established.");

            // Create a new thread for sending messages
            threadPool.submit(new SendMessageTask(out));

            // Create a new thread for receiving messages
            threadPool.submit(new ReceiveMessageTask(in));

        } catch (IOException e) {
            System.err.println("Failed to open connection: " + e.getMessage());
        }
    }

    private static class SendMessageTask implements Runnable {
        private OutputStream out;
        private Scanner scanner;

        public SendMessageTask(OutputStream out) {
            this.out = out;
            this.scanner = new Scanner(System.in);
        }

        @Override
        public void run() {
            try {
                while (true) {
                    System.out.println("Please enter a command (C, S, B, R):");
                    String command = scanner.nextLine().toUpperCase();

                    System.out.println("Sending:");
                    if (command.equals("R")) {
                        String timestamp = new SimpleDateFormat("HH:mm:ss").format(new Date());
                        System.out.print(timestamp + "_");

                        // Hardcoded route string for demonstration
                        String route = "000060_180060_330060_330000_420000_450000_450150_510150_510210_570210_360210_330210_300210_000210_000000";
                        System.out.println(route);
                        out.write((timestamp + "_" + route).getBytes());
                        out.flush();
                    } else {
                        String timestamp = new SimpleDateFormat("HH:mm:ss").format(new Date());
                        System.out.println(timestamp + "_" + command);
                        out.write((timestamp + "_" + command + "\n").getBytes());
                        out.flush();
                    }

                    if (command.equals("A")) {
                        break;
                    }
                }
            } catch (IOException e) {
                System.err.println("Failed to send command: " + e.getMessage());
            } finally {
                scanner.close();
                closeOutputStream(out);
            }
        }
    }

    private static class ReceiveMessageTask implements Runnable {
        private InputStream in;

        public ReceiveMessageTask(InputStream in) {
            this.in = in;
        }

        @Override
        public void run() {
            try {
                Scanner scanner = new Scanner(in);
                while (scanner.hasNextLine()) {
                    System.out.println("Received data:");
                    String data = scanner.nextLine();
                    System.out.println(data);
                }
                scanner.close();
            } catch (Exception e) {
                System.err.println("Failed to receive data: " + e.getMessage());
            } finally {
                closeInputStream(in);
            }
        }
    }

    private static void closeOutputStream(OutputStream out) {
        try {
            if (out != null) {
                out.close();
            }
        } catch (IOException e) {
            System.err.println("Failed to close output stream: " + e.getMessage());
        }
    }

    private static void closeInputStream(InputStream in) {
        try {
            if (in != null) {
                in.close();
            }
        } catch (IOException e) {
            System.err.println("Failed to close input stream: " + e.getMessage());
        }
    }
}
