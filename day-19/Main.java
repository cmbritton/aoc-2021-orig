import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.concurrent.TimeUnit;

public class Main {

    public static void main(String[] args) {
        Main main = new Main();
        main.run();
    }

    public void run() {
        Simulator simulator = new Simulator();
        simulator.run();
    }

    private class Simulator {

        private Map<String, Scanner> scanners = new HashMap<>();

        private void initData() {

            try (BufferedReader file = new BufferedReader(new FileReader("day-19/data.txt"))) {
                List<int[]> beacons = null;
                String scannerName = null;
                String line;
                while ((line = file.readLine()) != null) {
                    if (line.startsWith("---")) {
                        if (null != beacons) {
                            scanners.put(scannerName, new Scanner(scannerName, beacons.toArray(new int[][]{ })));
                        }
                        beacons = new ArrayList<>();
                        scannerName = "scanner " + line.split(" ")[2];
                        continue;
                    }
                    if (!line.isBlank()) {
                        String values[] = line.split(",");
                        beacons.add(new int[]{ Integer.parseInt(values[0]), Integer.parseInt(values[1]),
                                Integer.parseInt(values[2]) });
                    }
                }
                scanners.put(scannerName, new Scanner(scannerName, beacons.toArray(new int[][]{ })));
                Scanner scanner = scanners.get("scanner 0");
                scanner.originPosition = new int[]{ 0, 0, 0 };
                scanner.rotationMatrix = new int[][]{
                        { 1, 0, 0 },
                        { 0, 1, 0 },
                        { 0, 0, 1 }
                };
            } catch (IOException e) {
                System.err.println("Error. msg = " + e.getMessage());
            }
            return;
        }

        private int findOverlaps(Scanner s1, Scanner s2) {
            int overlapCount = 0;
            for (int[][] rotationMatrix : Scanner.ROTATIONS) {
                Scanner rs2 = s2.rotate(rotationMatrix);
                int overlaps = s1.computeCommonBeacons(rs2);
                if (overlaps > overlapCount) {
                    overlapCount = overlaps;
                    if (overlaps >= Scanner.MINIMUM_COMMON_BEACONS) {
                        s2.rotationMatrix = rotationMatrix;
                        s2.beacons = rs2.beacons;
                        s2.commonIndexes = rs2.commonIndexes;
                        int s1_common_index = s1.commonIndexes.get(s2.name)[0];
                        int s2_common_index = s2.commonIndexes.get(s1.name)[0];
                        if (null == s2.originPosition) {
                            s2.originPosition = new int[]{ 0, 0, 0 };
                        }
                        for (int i = 0; i < 3; ++i) {
                            s2.originPosition[i] =
                                    s1.originPosition[i] - (rs2.beacons[s2_common_index][i] - s1.beacons[s1_common_index][i]);
                        }
                        break;
                    }
                }
            }
            return overlapCount;
        }

        private boolean done() {
            for (Scanner scanner : this.scanners.values()) {
                if (!scanner.isOriented()) {
                    return false;
                }
            }
            return true;
        }

        private void findOverlappingBeacons() {
            while (!done()) {
                for (String s1Name : this.scanners.keySet()) {
                    for (String s2Name : this.scanners.keySet()) {
                        if (s1Name.equals(s2Name)) {
                            continue;
                        }
                        Scanner s1 = this.scanners.get(s1Name);
                        Scanner s2 = this.scanners.get(s2Name);
                        if (!s1.isOriented() && s2.isOriented()){
                            Scanner tmp = s1;
                            s1 = s2;
                            s2 = tmp;
                        }
                        if (s1.isOriented() && !s2.isOriented()) {
                            findOverlaps(s1, s2);
                        }
                    }
                }
            }
            return;
        }

        private void run() {
            long startTimeMillis = System.currentTimeMillis();
            initData();
            findOverlappingBeacons();
            Set<int[]> beacons = new HashSet<>();
            for (String scannerName : this.scanners.keySet()) {
                for (int[] beacon : this.scanners.get(scannerName).beacons) {
                    if (null != this.scanners.get(scannerName).originPosition) {
                        if (null != this.scanners.get(scannerName).rotationMatrix) {
                            int[] translatedBeacon = this.scanners.get(scannerName).translate(beacon);
                            if (-1 == this.scanners.get(scannerName).find(translatedBeacon,
                                    beacons.toArray(new int[][] {}))) {
                                beacons.add(translatedBeacon);
                            }
                        }
                    }
                }
            }
            long endTimeMillis = System.currentTimeMillis();
            System.err.println("beacon count: " + beacons.size());
            System.err.println("Elapsed time: " + elapsedTime(startTimeMillis, endTimeMillis));
            return;
        }

        private String elapsedTime(long startTimeMillis, long endTimeMillis) {
            long elapsedMillis = endTimeMillis - startTimeMillis;
            final long hr = TimeUnit.MILLISECONDS.toHours(elapsedMillis);
            final long min = TimeUnit.MILLISECONDS.toMinutes(elapsedMillis - TimeUnit.HOURS.toMillis(hr));
            final long sec = TimeUnit.MILLISECONDS.toSeconds(elapsedMillis - TimeUnit.HOURS.toMillis(hr) - TimeUnit.MINUTES.toMillis(min));
            final long ms = TimeUnit.MILLISECONDS.toMillis(elapsedMillis - TimeUnit.HOURS.toMillis(hr) - TimeUnit.MINUTES.toMillis(min) - TimeUnit.SECONDS.toMillis(sec));
            return String.format("%02d:%02d:%02d.%03d", hr, min, sec, ms);
        }
    }


    private class Scanner {

        private static final int MINIMUM_COMMON_BEACONS = 12;

        private static final int[][][] ROTATIONS = new int[][][]{
                {
                        { 1, 0, 0 },
                        { 0, 0, -1 },
                        { 0, 1, 0 },
                },
                {
                        { 1, 0, 0 },
                        { 0, -1, 0 },
                        { 0, 0, -1 }
                },
                {
                        { 1, 0, 0 },
                        { 0, 0, 1 },
                        { 0, -1, 0 }
                },
                {
                        { 0, 0, 1 },
                        { 0, 1, 0 },
                        { -1, 0, 0 }
                },
                {
                        { -1, 0, 0 },
                        { 0, 1, 0 },
                        { 0, 0, -1 }
                },
                {
                        { 0, 0, -1 },
                        { 0, 1, 0 },
                        { 1, 0, 0 }
                },
                {
                        { 0, -1, 0 },
                        { 1, 0, 0 },
                        { 0, 0, 1 }
                },
                {
                        { -1, 0, 0 },
                        { 0, -1, 0 },
                        { 0, 0, 1 }
                },
                {
                        { 0, 1, 0 },
                        { -1, 0, 0 },
                        { 0, 0, 1 }
                },
                {
                        { 1, 0, 0 },
                        { 0, 1, 0 },
                        { 0, 0, 1 }
                },
                {
                        { 0, 0, 1 },
                        { 1, 0, 0 },
                        { 0, 1, 0 }
                },
                {
                        { -1, 0, 0 },
                        { 0, 0, 1 },
                        { 0, 1, 0 }
                },
                {
                        { 0, 0, -1 },
                        { -1, 0, 0 },
                        { 0, 1, 0 }
                },
                {
                        { 0, -1, 0 },
                        { 0, 0, -1 },
                        { 1, 0, 0 }
                },
                {
                        { -1, 0, 0 },
                        { 0, 0, -1 },
                        { 0, -1, 0 }
                },
                {
                        { 0, 1, 0 },
                        { 0, 0, -1 },
                        { -1, 0, 0 }
                },
                {
                        { 0, 0, 1 },
                        { 0, -1, 0 },
                        { 1, 0, 0 }
                },
                {
                        { 0, 0, -1 },
                        { 0, -1, 0 },
                        { -1, 0, 0 }
                },
                {
                        { 0, -1, 0 },
                        { -1, 0, 0 },
                        { 0, 0, -1 }
                },
                {
                        { 0, 1, 0 },
                        { 1, 0, 0 },
                        { 0, 0, -1 }
                },
                {
                        { 0, 0, 1 },
                        { -1, 0, 0 },
                        { 0, -1, 0 }
                },
                {
                        { 0, 0, -1 },
                        { 1, 0, 0 },
                        { 0, -1, 0 }
                },
                {
                        { 0, -1, 0 },
                        { 0, 0, 1 },
                        { -1, 0, 0 }
                },
                {
                        { 0, 1, 0 },
                        { 0, 0, 1 },
                        { 1, 0, 0 }
                }
        };

        private String name = null;
        private int[][] beacons = null;
        private int[] originPosition = null;
        private int[][] rotationMatrix = null;
        private Map<String, int[]> commonIndexes = new HashMap<>();

        private Scanner(String name, int[][] beacons) {
            this.name = name;
            this.beacons = beacons;
        }

        private static int[] rotateBeacon(int[][] rotationMatrix, int[] beacon) {

            int[] rotatedBeacon = new int[3];
            for (int i = 0; i < 3; ++i) {
                int result = 0;
                for (int j = 0; j < 3; ++j) {
                    result += rotationMatrix[i][j] * beacon[j];
                }
                rotatedBeacon[i] = result;
            }
            return rotatedBeacon;
        }

        private boolean isOriented() {
            return null != this.rotationMatrix;
        }

        private Scanner rotate(int[][] rotationMatrix) {

            List<int[]> rotatedBeacons = new ArrayList<>();
            for (int[] beacon : this.beacons) {
                rotatedBeacons.add(rotateBeacon(rotationMatrix, beacon));
            }
            Scanner rotated_scanner = new Scanner(this.name, rotatedBeacons.toArray(new int[][] {}));
            rotated_scanner.rotationMatrix = rotationMatrix;
            rotated_scanner.originPosition = this.originPosition;
            return rotated_scanner;
        }

        private int[] translate(int[] beacon) {
            return new int[]{ beacon[0] + this.originPosition[0],
                    beacon[1] + this.originPosition[1],
                    beacon[2] + this.originPosition[2]
            };
        }

        private int find(int[] beacon, int[][] beacons) {

            for (int i = 0; i < beacons.length; ++i) {
                if ((beacons[i][0] == beacon[0]) && (beacons[i][1] == beacon[1]) && (beacons[i][2] == beacon[2])) {
                    return i;
                }
            }
            return -1;
        }

        private int computeCommonBeacons(Scanner other) {

            List<Integer> commonIndexesSelf = new ArrayList<>();
            List<Integer> commonIndexesOther = new ArrayList<>();
            for (int[] b1Self : this.beacons) {
                for (int[] b2Self : this.beacons) {
                    if (b1Self == b2Self) {
                        continue;
                    }
                    for (int[] b1Other : other.beacons) {
                        for (int[] b2Other : other.beacons) {
                            if (b1Other == b2Other) {
                                continue;
                            }
                            if (((b1Self[0] - b2Self[0]) - (b1Other[0] - b2Other[0])) == 0 &&
                                    ((b1Self[1] - b2Self[1]) - (b1Other[1] - b2Other[1])) == 0 &&
                                    ((b1Self[2] - b2Self[2]) - (b1Other[2] - b2Other[2])) == 0) {
                                int idx = find(b1Self, this.beacons);
                                if (!commonIndexesSelf.contains(idx)) {
                                    commonIndexesSelf.add(idx);
                                }
                                idx = find(b2Self, this.beacons);
                                if (!commonIndexesSelf.contains(idx)) {
                                    commonIndexesSelf.add(idx);
                                }
                                idx = find(b1Other, other.beacons);
                                if (!commonIndexesOther.contains(idx)) {
                                    commonIndexesOther.add(idx);
                                }
                                idx = find(b2Other, other.beacons);
                                if (!commonIndexesOther.contains(idx)) {
                                    commonIndexesOther.add(idx);
                                }
                                if (commonIndexesSelf.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                                    if (commonIndexesOther.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                                        break;
                                    }
                                }
                            }
                            if (commonIndexesSelf.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                                if (commonIndexesOther.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                                    break;
                                }
                            }
                        }
                        if (commonIndexesSelf.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                            if (commonIndexesOther.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                                break;
                            }
                        }
                    }
                    if (commonIndexesSelf.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                        if (commonIndexesOther.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                            break;
                        }
                    }
                }
            }
            if (commonIndexesSelf.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                this.commonIndexes.put(other.name, commonIndexesSelf.stream().mapToInt(i -> i).toArray());
            }

            if (commonIndexesOther.size() >= Scanner.MINIMUM_COMMON_BEACONS) {
                other.commonIndexes.put(this.name, commonIndexesOther.stream().mapToInt(i -> i).toArray());
            }

            return commonIndexesSelf.size();
        }
    }
}