import java.io.*;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) throws IOException, InterruptedException {
        File inputFile = new File("./dane.txt");
        File outputFile = new File("./wynik.txt");
        long lastModified = outputFile.lastModified();
        Scanner scanner = new Scanner(System.in);
        System.out.println("Podaj liczbe: ");
        int number = scanner.nextInt();
        BufferedWriter writer = new BufferedWriter(new FileWriter(inputFile));
        writer.write(String.valueOf(number));
        writer.close();
        while (true) {
            Thread.sleep(500);
            if (outputFile.lastModified() > lastModified) {
                BufferedReader reader = new BufferedReader(new FileReader(outputFile));
                String line = reader.readLine();
                System.out.println("Wynik: " + line);
                return;
            }
        }


    }
}
