import java.io.*;

public class Server {
    public static void main(String[] args) throws InterruptedException, IOException {
        int result = 0;
        File inputFile = new File("./dane.txt");
        File outputFile = new File("./wynik.txt");
        if(!inputFile.exists()) {
            System.out.println("File does not exist");
            return;
        }
        long lastModified = inputFile.lastModified();
        while (true) {
            Thread.sleep(500);
            long currentModified = inputFile.lastModified();
            if (currentModified > lastModified) {
                lastModified = currentModified;
                BufferedReader reader = new BufferedReader(new FileReader(inputFile));
                String line = reader.readLine();
                int number = Integer.parseInt(line);
                System.out.println("Otrzymano liczbę: " + number);
                result = number * 3;
                BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));
                writer.write(String.valueOf(result));
                writer.close();
            }
        }
    }
}
