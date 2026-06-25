<script setup>
  import { ref } from "vue";
  const fileInput = ref(null);
  const browseFile = () => {
    fileInput.value.click();
  };

  const handleFiles = (event) => {
    const files = event.target.files;
    console.log(files);
  };
</script>

<template><br>
  <div class="row">
      <div class="col">
        
      </div>
      <div class="col"></div>
    </div>

   <br> <br>
  <div class="card">
    <h2>Style Classifier</h2>
    <div class="drop-zone" @click="browseFile">
        <div class="icon">📄⬆️</div>
        <p>
          <strong>Drag & Drop</strong><br />
          Multi-file PGNs here<br />
          or<br />
          <span class="browse">[Click to Browse]</span>
        </p>
        <input
        ref="fileInput"
        type="file"
        accept=".pgn"
        multiple
        webkitdirectory
        @change="selectFiles"
        style="display:none"
        />
    </div>

    <button class="upload-btn">Upload & Classify</button>
    <p class="subtitle">Analyze a collection of your Chess Games.</p>
  </div>
</template>

<style scoped>
    .card {
      width: 320px;
      padding: 20px;
      border-radius: 20px;
      background: #2e7d32;
      color: white;
      text-align: center;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }

    h2 {
      font-size: 18px;
      margin-bottom: 15px;
    }

    .drop-zone {
      border: 2px dashed rgba(255, 255, 255, 0.6);
      border-radius: 15px;
      padding: 25px;
      cursor: pointer;
      transition: 0.3s;
    }

    .drop-zone:hover {
      background: rgba(255, 255, 255, 0.1);
    }

    .icon {
      font-size: 40px;
      margin-bottom: 10px;
    }

    .browse {
      text-decoration: underline;
      cursor: pointer;
    }

    .upload-btn {
      margin-top: 15px;
      width: 100%;
      padding: 10px;
      border: none;
      border-radius: 12px;
      background: white;
      color: #2e7d32;
      font-weight: bold;
      cursor: pointer;
      transition: 0.3s;
    }

    .upload-btn:hover {
      background: #f0f0f0;
    }

    .subtitle {
      margin-top: 10px;
      font-size: 12px;
      opacity: 0.8;
    }
</style>