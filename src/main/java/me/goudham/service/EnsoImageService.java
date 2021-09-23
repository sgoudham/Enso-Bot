package me.goudham.service;

import jakarta.inject.Singleton;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.color.ColorSpace;
import java.awt.image.BufferedImage;
import java.awt.image.ColorConvertOp;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import javax.imageio.ImageIO;

@Singleton
public class EnsoImageService implements ImageService {

    @Override
    public BufferedImage resizeImage(BufferedImage bufferedImage, int height, int width) {
        Image tempImage = bufferedImage.getScaledInstance(width, height, Image.SCALE_SMOOTH);
        BufferedImage resizedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);

        Graphics2D g2d = resizedImage.createGraphics();
        g2d.drawImage(tempImage, 0, 0, null);
        g2d.dispose();

        return resizedImage;
    }

    @Override
    public byte[] toByteArray(BufferedImage bufferedImage, String fileFormat) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ImageIO.write(bufferedImage, fileFormat, baos);
        return baos.toByteArray();
    }

    @Override
    public BufferedImage toImage(byte[] bytes) throws IOException {
        InputStream inputStream = new ByteArrayInputStream(bytes);
        return ImageIO.read(inputStream);
    }

    @Override
    public BufferedImage toGrayscaleImage(BufferedImage bufferedImage) throws IOException {
        ColorConvertOp colorConvertOp = new ColorConvertOp(ColorSpace.getInstance(ColorSpace.CS_GRAY), null);
        BufferedImage grayscaleImage = colorConvertOp.filter(bufferedImage, null);
        ByteArrayOutputStream os = new ByteArrayOutputStream();
        ImageIO.write(grayscaleImage, "png", os);
        return grayscaleImage;
    }

    @Override
    public void invertImage(BufferedImage bufferedImage) {
        for (int x = 0; x < bufferedImage.getWidth(); x++) {
            for (int y = 0; y < bufferedImage.getHeight(); y++) {
                int rgba = bufferedImage.getRGB(x, y);
                Color col = new Color(rgba, true);
                col = new Color(255 - col.getRed(),255 - col.getGreen(),255 - col.getBlue());
                bufferedImage.setRGB(x, y, col.getRGB());
            }
        }
    }
}
