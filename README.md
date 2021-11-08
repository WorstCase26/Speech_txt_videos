# Video downloader and Speech to Text conversion tool
<!--
*** Thanks for checking out the ResumeTool. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".

***

***

***

<br />
<!-- TABLE OF CONTENTS -->

<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>




<!-- ABOUT THE PROJECT -->

## About The Project
This script will download a video from YouTube using the PyTube package. It will then seperate the audio file (.wav) from the other components of the video file (mp4). The scipt then uses the Google API to convert the sound in the video to a text transcript. The output is an excel file with the translated text. 


### Built With

* Spyder IDE (https://www.spyder-ide.org/)



<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

These are the only Python packages in the requirements for this application to run.


pytube
SpeechRecognition
moviepy
wave
contextlib

### Installation

1. Clone the repo

   ```sh
   git clone 
   ```

2. Install packages with windows

   ```sh
    pip install pytube
    pip install SpeechRecognition
    pip install moviepy
    pip install wave
    pip install contextlib
   ```

<!-- USAGE EXAMPLES -->

## Usage

This tool would be very useful for converting a video to a text transcript.

<!-- ROADMAP -->

## Roadmap

See the [open issues](https://github.com/HawaiiDive/HawaiiDive/ResumeTool/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- CONTACT -->

## Contact

Project Link: 

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements
* [https://github.com/HawaiiDive]
