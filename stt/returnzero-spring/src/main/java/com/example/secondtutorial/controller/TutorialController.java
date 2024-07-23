package com.example.secondtutorial.controller;


import com.example.secondtutorial.service.TutorialService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.sound.sampled.UnsupportedAudioFileException;
import java.io.IOException;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/tutorial")
public class TutorialController {
    private final TutorialService tutorialService;

    @PostMapping(value = "/transcribe/file", consumes = {MediaType.MULTIPART_FORM_DATA_VALUE})
    public void transcribeFile(@RequestPart MultipartFile file) throws IOException, InterruptedException {
        tutorialService.transcribeFile(file);
    }

    @PostMapping(value = "/transcribe/websocket/file", consumes = {MediaType.MULTIPART_FORM_DATA_VALUE})
    public void transcribeWebsocketFile(@RequestPart MultipartFile file) throws IOException, UnsupportedAudioFileException, InterruptedException {
        tutorialService.transcribeWebSocketFile(file);
    }
}




