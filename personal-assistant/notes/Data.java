import java.io.*; //file
import java.util.*; //Date, ArrayList
import java.awt.*; //clipboard 
import java.awt.datatransfer.*; //more clipboard 

public class Data {
    
    public static void usage() {
        System.err.println("usage: Data\nusage: Data [-?/-d/-e/-r]\nusage: Data [-a] <message>");
        System.exit(0);
    }
    
    public static void uiUsage() {
        System.out.println("    ?: Help command.");
        System.out.println("    a: Type and append text.");
        System.out.println("    c: Clear the screen.");
        System.out.println("    d: View all entries.");
        System.out.println("    e: Edit a specified line.");
        System.out.println("    r: Remove a specified line.");
        System.out.println("    x: Exit the program.");
        System.out.println("    1: Enable auto-append");
        System.out.println("    2: Disable auto-append");
    }
    
    private static ArrayList<String> lines = null;
    public static final int REMOVE = 0;
    public static final int EDIT = 1;
    
    /**
     * Loads lines into 'lines'
     */
    public static void loadLines() throws Exception {
        
        lines = new ArrayList<String>(); //Reset, and load most current from file
        
        BufferedReader r = new BufferedReader(new FileReader("notes.txt"));
        String line;
        while( (line = r.readLine()) != null) {
            lines.add(line);
        }
    }
    
    /**
     * Display lines from file
     */
    public static void showLines() {
        for(int idx = 0; idx < lines.size(); ++idx) {
            String line = lines.get(idx);
            String time = getTime(line);
            line = removeTime(line);
            System.out.printf("%04d: %s: ", idx, time);
            
            /*Spacing to come later */
            System.out.println(line);
        }
    }
    
    private static String removeTime(String n) {
        String[] sep = n.split((char)0x1F + "");
        if(sep.length == 1)
           return n;
        return sep[1];
    }
    
    private static String getTime(String n) {
        String d = "NO TIME DATA FOUND";
        String[] sep = n.split((char)0x1F + "");
        if(sep.length == 1)
            return d;
        
        try {
            d = new Date(Long.parseLong(sep[0])).toString();
        } catch(NumberFormatException e) { /**/ }
            
        return d;
    }
    
    private static long getTimeVal(String n) {
       String[] sep = n.split((char)0x1F + "");
       if(sep.length == 1)
           return 0;
       try {
            return Long.parseLong(sep[0]);
       } catch(NumberFormatException e) { return 0; }
    }
    
    /**
     * Write a line to the file
     */
    public static void writeLine(String line) throws Exception {
        String s = System.currentTimeMillis() + "" + (char)0x1F + line;
        lines.add(s);
        clearAndWriteAll();
        System.out.println("Append successful. (" + (lines.size() - 1) + ")");
    }
    
    /**
     * Write some args to the file
     */
    public static void writeArgs(String[] args) throws Exception {
        String tot = "";
        for(int idx = 1; idx < args.length; ++idx) {
            tot += (args[idx] + " ");
        }
        writeLine(tot);
    }
    
    private static void clearAndWriteAll() throws Exception {
        BufferedWriter w = new BufferedWriter(new FileWriter("notes.txt", false));
        for(int idx = 0; idx < lines.size(); ++idx) {
            w.write(lines.get(idx));
            w.newLine();
        }
        w.close();
    }
    
    public static void clear() throws Exception {
        new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor(); //Cygwin moment
    }    
    
    public static void promptUserAndModifyLines(int mode) throws Exception {
        
        if(mode != REMOVE && mode != EDIT)
            throw new IllegalArgumentException("Bad mode");
        
        Scanner sc = new Scanner(System.in);
        int n = -1;
        
        while( (n < 0 || n >= lines.size())) {
            n = -1;
            System.out.print("Line: ");
            try {
                n = Integer.parseInt(sc.nextLine());
            } catch(NumberFormatException e) {
                System.err.println("Invalid Input"); 
                continue;
            };
            
            if(n < 0 || n >= lines.size())
                System.err.println("Invalid Line");
        }

        String line = removeTime(lines.get(n));
        long time = getTimeVal(lines.get(n));
        StringSelection selection = new StringSelection(line);
        Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
        clipboard.setContents(selection, selection);
        System.out.println("Line " + n + " copied to clipboard. <" + line.trim() + ">");
        
        if(mode == EDIT) {
            System.out.print("New Data? [Empty to ignore]: ");
            String add = sc.nextLine();
            if(add == null || add.isEmpty())
                return;
            else
                lines.set(n, time + "" + ((char)0x1F) + add);
        }
        else if(mode == REMOVE) {
            System.out.println("Remove this line? [Y/N]");
            String r = sc.nextLine();
            if(r == null || r.isEmpty() || r.toUpperCase().charAt(0) != 'Y')
                return;
            lines.remove(n);
        }
        
        clearAndWriteAll(); //flush
        loadLines(); 
        System.out.println(mode == EDIT ? "Updated successfully." : "Removed successfully.");
    }

    public static void main(String[] args) throws Exception {
        
		try {
			new File("notes.txt").createNewFile(); //will fail if exists
		} catch(Exception e) { /*Nothing to do here...*/ }
		
		loadLines(); //setup

        if(args.length != 0) { //Operating straight from the command line
            if(args.length == 1) { // -d, -?, -e, -r;
                if(args[0].equals("-d"))
                    showLines();
                else if(args[0].equals("-e"))
                    promptUserAndModifyLines(EDIT);
                else if(args[0].equals("-r"))
                    promptUserAndModifyLines(REMOVE);
                else //-? or error
                    usage();
            }
            else {
                if(args[0].equals("-a")) 
                    writeArgs(args);
                else
                    usage();
            }
            return;
        }
        
        //Otherwise, load the UI
        clear();
        System.out.println("LOAD OK.\nTime: " + new Date().toString());
        boolean done = false;
        boolean isAutoAppend = false;
        Scanner sc = new Scanner(System.in);
        while(!done) {
            System.out.print("Do:" + (isAutoAppend ? " (Automatic Mode): " : " "));
            String choice = sc.nextLine();
            if(choice == null || choice.isEmpty() || choice.endsWith("8"))
                continue;
            
            if(isAutoAppend) {
                if(choice.equals("2"))
                    isAutoAppend = false;
                else if(choice.equals("x"))
                    done = true;
                else if(choice.equals("r"))
                    promptUserAndModifyLines(REMOVE);
                else if(choice.equals("?")){
                    System.out.println("    2: Disable Auto-Append.");
                    System.out.println("    r: Remove a specified line.");
                    System.out.println("    x: Exit the program.");
                    System.out.println("    ?: Help command");
                }
                else {
                    writeLine(choice);
                }
                continue;
            }
            
            if(choice.equals("?"))
                uiUsage();
            else if(choice.startsWith("a")) {
                if(choice.length() >= 3 && choice.substring(0,2).equals("a ")) {
                    writeLine(choice.substring(2, choice.length()));
                }
            }
            else if(choice.equals("c"))
                clear();
            else if(choice.equals("d"))
                showLines();
            else if(choice.equals("e"))
                promptUserAndModifyLines(EDIT);
            else if(choice.equals("r"))
                promptUserAndModifyLines(REMOVE);
            else if(choice.equals("x"))
                done = true;
            else if(choice.equals("1"))
                isAutoAppend = true;
            else
                uiUsage();
        }
        sc.close(); 
    }
}