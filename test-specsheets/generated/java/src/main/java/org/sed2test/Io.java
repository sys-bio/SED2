package org.sed2test;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/** Top-level read/write entry points for libsed2test. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Io {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    static {
        RulesData.register();
    }

    private Io() {}

    public static TestDocument readFromString(String text) throws IOException {
        JsonNode raw = MAPPER.readTree(text);
        TestDocument obj = new TestDocument();
        Dispatch.loadFields(obj, raw);
        obj.attach(null, obj);
        return obj;
    }

    public static TestDocument readFromFile(String path) throws IOException {
        String text = Files.readString(Path.of(path), StandardCharsets.UTF_8);
        return readFromString(text);
    }

    public static String writeToString(TestDocument doc) {
        try {
            return MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(doc.toJsonValue());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static void writeToFile(TestDocument doc, String path) throws IOException {
        Files.writeString(Path.of(path), writeToString(doc), StandardCharsets.UTF_8);
    }
}
