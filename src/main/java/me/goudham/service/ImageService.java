package me.goudham.service;

import java.awt.image.BufferedImage;
import java.io.IOException;

public interface ImageService {
    BufferedImage resizeImage(BufferedImage bufferedImage, int height, int width);
    byte[] toByteArray(BufferedImage bufferedImage, String fileFormat) throws IOException;
    BufferedImage toImage(byte[] bytes) throws IOException;
    BufferedImage toGrayscaleImage(BufferedImage bufferedImage) throws IOException;
    void invertImage(BufferedImage bufferedImage);
}
