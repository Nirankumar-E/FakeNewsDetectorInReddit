<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Cyber Sign-In</title>
  <link rel="stylesheet" href="sign-in/sign-in.css" />
  <!-- Add Font Awesome CDN for GitHub icons -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
</head>

<body>
  <div class="background"></div>
  <main class="form-signin">
    <form method="post" id="detection-form">
      <h1 class="title">Fake News detection</h1>

      <div class="form-floating">
        <input type="text" placeholder="url:example.com" name="url" />
      </div>

      <div class="form-floating">
        <input type="text" placeholder="Reddit Title" name="title"  />
      </div>

      <button type="submit" id="submit-button">Check</button>

      <p class="footer">&copy; 2025–2026</p>
    </form>
    <div class="github-links">
        <a href="https://github.com/Ayyappan1502" class="github-link" data-username="Ayyappan1502" target="_blank">
            <i class="fab fa-github"></i>
            <div class="tooltip"></div>
        </a>
        <a href="https://github.com/Silambaraselvan-15" class="github-link" data-username="Silambaraselvan-15" target="_blank">
            <i class="fab fa-github"></i>
            <div class="tooltip"></div>
        </a>
        <a href="https://github.com/BayanFahim14" class="github-link" data-username="BayanFahim14" target="_blank">
            <i class="fab fa-github"></i>
            <div class="tooltip"></div>
        </a>
        <a href="https://github.com/Nirankumar-E" class="github-link" data-username="Nirankumar-E" target="_blank">
            <i class="fab fa-github"></i>
            <div class="tooltip"></div>
         </a>
</div>
<style>
 
    .github-links {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
  position: relative;
}

.github-link {
  position: relative;
  font-size: 30px;
  color: #333;
  text-decoration: none;
}

    .github-links a:hover {
      color: #000;
    }
 

.github-link .tooltip {
  position: absolute;
  bottom: 120%;
  left: 50%;
  transform: translateX(-50%);
  display: none;
  flex-direction: column;
  align-items: center;
  padding: 10px 15px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
  font-size: 12px;
  z-index: 100;
  min-width: 140px;
}


.github-link .tooltip img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-bottom: 8px;
}

.github-link:hover .tooltip {
  display: flex;
}

  </style>

    <!-- Result container -->
    <div id="result-container" style="display: none;">
      <?php
      function detect($input)
      {
        // Command to execute the Python script
        $command = "python3 detector.py \"$input\"";

        // Execute the command and capture the output and errors
        $output = [];
        $return_var = 0;
        exec($command . " 2>&1", $output, $return_var);

        // Return the output as a string
        return implode("\n", $output);
      }

      if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Check if 'title' or 'url' is provided
        if (!empty($_POST['title'])) {
            $getInput = $_POST['title'];
            echo "<h3>Result:</h3><br>\n";
            echo "\n<br><pre>" . detect($getInput) . "</pre>";
        } elseif (!empty($_POST['url'])) {
            $getInput = $_POST['url'];
            echo "<h3>Result:</h3><br>\n";
            echo "\n<br><pre>" . detect($getInput) . "</pre>";
        } else {
            // If neither 'title' nor 'url' is provided
            echo "<h3>Error:</h3><br>\n";
            echo "Please provide either a title or a URL.";
        }
      }
      ?>
    </div>

    
  </main>

  <style>
    .form-signin {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
    }

    #result-container {
      margin-top: 20px;
      padding: 15px;
      border: 1px solid #ccc;
      border-radius: 8px;
      background-color: #00ff99;
      width: 100%;
      max-width: 600px;
      text-align: left;
      font-family: Arial, sans-serif;
      font-size: 14px;
      color: black;
    }

    .github-links {
      display: flex;
      justify-content: center;
      gap: 10px;
      margin-top: 20px;
      position: relative;
    }

    .github-link {
      position: relative;
      font-size: 30px;
      color: #333;
      text-decoration: none;
    }

    .github-links a:hover {
      color: #000;
    }

    .github-link .tooltip {
      position: absolute;
      bottom: 120%;
      left: 50%;
      transform: translateX(-50%);
      display: none;
      flex-direction: column;
      align-items: center;
      padding: 10px 15px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.15);
      box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.3);
      color: #fff;
      font-size: 12px;
      z-index: 100;
      min-width: 140px;
    }

    .github-link .tooltip img {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      margin-bottom: 8px;
    }

    .github-link:hover .tooltip {
      display: flex;
    }
  </style>

  <script>
    const form = document.getElementById('detection-form');
    const resultContainer = document.getElementById('result-container');
    const submitButton = document.getElementById('submit-button');

    form.addEventListener('submit', () => {
      // Hide the result container while processing
      resultContainer.style.display = 'none';

      // Disable the submit button to prevent multiple submissions
      submitButton.disabled = true;
    });

    window.addEventListener('load', () => {
      // Show the result container if it contains content
      if (resultContainer.innerHTML.trim() !== '') {
        resultContainer.style.display = 'block';
      }

      // Re-enable the submit button
      submitButton.disabled = false;
    });
  </script>

</body>

</html>
