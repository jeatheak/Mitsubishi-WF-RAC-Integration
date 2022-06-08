package src.refactor;

import java.nio.ByteBuffer;
import java.util.Arrays;

public class Utils {
    public static ByteBuffer toBytes(int[] iArr) {
        ByteBuffer allocate = ByteBuffer.allocate(iArr.length);
        for (int i : iArr) {
            allocate.put(toByte(i));
        }
        return allocate;
    }

    public static int getMatch(ByteBuffer compareByteBuffer, int[]... inputMatrix) {
        for (int i = 0; i < inputMatrix.length; i++)
            if (compare(inputMatrix[i], compareByteBuffer))
                return i;

        return -1;
    }

    public static boolean compare(int[] inputArray1, ByteBuffer bytebuffer) {
        return Utils.equal(Utils.toBytes(inputArray1), bytebuffer);
    }

    public static boolean equal(ByteBuffer byteBuffer, ByteBuffer byteBuffer2) {
        return Arrays.equals(byteBuffer.array(), byteBuffer2.array());
    }

    public static boolean equal(int[] byteBuffer, ByteBuffer byteBuffer2) {
        return Arrays.equals(toBytes(byteBuffer).array(), byteBuffer2.array());
    }

    public static boolean equal(int[] byteBuffer, int[] byteBuffer2) {
        return Arrays.equals(toBytes(byteBuffer).array(), toBytes(byteBuffer2).array());
    }

    public static byte toByte(int i) {
        return Arrays.copyOfRange(ByteBuffer.allocate(4).putInt(i).array(), 3, 4)[0];
    }

    public static ByteBuffer and(int[] byteBuffer, ByteBuffer byteBuffer2) {
        return and(toBytes(byteBuffer), byteBuffer2);
    }

    public static ByteBuffer and(int[] byteBuffer, int[] byteBuffer2) {
        return and(toBytes(byteBuffer), toBytes(byteBuffer2));
    }

    public static ByteBuffer and(ByteBuffer byteBuffer, ByteBuffer byteBuffer2) {
        int length = byteBuffer.array().length;
        byteBuffer.rewind();
        byteBuffer2.rewind();
        ByteBuffer allocate = ByteBuffer.allocate(length);
        for (int i = 0; i < length; i++) {
            allocate.put((byte) (byteBuffer.get() & byteBuffer2.get()));
        }
        return allocate;
    }
}
