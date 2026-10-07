package dev.journey;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
@SpringBootTest(properties="ai.mode=demo") @AutoConfigureMockMvc
class ApiTest {
 @Autowired MockMvc mvc;
 @Test void validInputReturnsLabeledDemo() throws Exception {mvc.perform(post("/api/run").contentType("application/json").content("{\"text\":\"How long are logs retained?\"}")).andExpect(status().isOk()).andExpect(jsonPath("$.mode").value("demo")).andExpect(jsonPath("$.result").exists());}
 @Test void blankInputIsRejected() throws Exception {mvc.perform(post("/api/run").contentType("application/json").content("{\"text\":\" \"}")).andExpect(status().isBadRequest());}
}
