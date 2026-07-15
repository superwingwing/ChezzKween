<script setup>
      import { ref } from "vue"
      const fileInput = ref(null)
      const folderInput = ref(null)
      const selectedFiles = ref([])
      const uploading = ref(false)
      const progress = ref(0)
      const browseFiles = () => {
        fileInput.value.click()
      }
      const browseFolder = () => {
        folderInput.value.click()
      }
      const selectFiles = (event) => {
        const files = Array.from(event.target.files)
        selectedFiles.value.push(...files)
        console.log(selectedFiles.value)
      }
      const uploadFiles = async () => {
        if (selectedFiles.value.length === 0) {
          alert("Please select PGN files.")
          return
        }
        uploading.value = true
        progress.value = 0
        const formData = new FormData()
        selectedFiles.value.forEach(file => {
          formData.append("files", file)
        })
        // Fake progress while waiting
        const timer = setInterval(() => {
          if (progress.value < 95) {
            progress.value += 5
          }
        }, 300)
        try {
          const response = await fetch(
            "http://127.0.0.1:8000/upload_style",
            {
              method: "POST",
              body: formData
            }
          )
          clearInterval(timer)
          progress.value = 100
          const result = await response.json()
          console.log(result)
          alert(`${result.games_uploaded} games uploaded`)
          setTimeout(() => {
            uploading.value = false
            progress.value = 0
          }, 800)
        } catch (error) {
          clearInterval(timer)
          uploading.value = false
          progress.value = 0
          console.error(error)
        }
    }
</script>

<template>
    <br><br>
    <div class="card">
        <h2>
          Style Classifier
        </h2>
        <div class="drop-zone">
          <div class="icon">
            📄⬆️
          </div>
          <p>
             <strong class="browse" @click="browseFiles">
              Select PGN Files
            </strong>
            <br>
                 or
            <br>
            <strong class="browse" @click="browseFolder">
              Select Folder
            </strong>
          </p>
          <p v-if="selectedFiles.length">
            {{ selectedFiles.length }} PGN file(s) selected
          </p>

          <!-- Select Multiple PGN Files -->
          <input
            ref="fileInput"
            type="file"
            accept=".pgn"
            multiple
            @change="selectFiles"
            style="display:none"
          />
          <!-- Select Folder -->
          <input
            ref="folderInput"
            type="file"
            accept=".pgn"
            webkitdirectory
            directory
            multiple
            @change="selectFiles"
            style="display:none"
          />
        </div>
        <button
            class="upload-btn"
            @click="uploadFiles"
            :disabled="uploading"
          >
            {{ uploading ? `Uploading... ${progress}%` : "Upload" }}
        </button>

          <div
            v-if="uploading"
            class="progress-container"
          >
            <div
              class="progress-bar"
              :style="{ width: progress + '%' }"
            ></div>
          </div>
          <p class="subtitle">
            Analyze a collection of your Chess Games.
          </p>
    </div>
</template>

<style scoped>
    .card {
      width: 320px;
      padding: 20px;
      border-radius: 20px;
      background: #2e7d32;
      color:white;
      text-align:center;
      box-shadow:0 10px 25px rgba(0,0,0,0.2);
    }

    h2 {
      font-size:18px;
      margin-bottom:15px;
    }

    .drop-zone {
      border:2px dashed rgba(255,255,255,0.6);
      border-radius:15px;
      padding:25px;
      cursor:pointer;
    }

    .drop-zone:hover {
      background:rgba(255,255,255,0.1);
    }

    .icon {
      font-size:40px;
      margin-bottom:10px;
    }



    .browse {
      text-decoration:underline;
      cursor:pointer;
    }

    .upload-btn {
      margin-top:15px;
      width:100%;
      padding:10px;
      border:none;
      border-radius:12px;
      background:white;
      color:#2e7d32;
      font-weight:bold;
      cursor:pointer;
    }

    .upload-btn:hover {
      background:#f0f0f0;
    }

    .subtitle {
      margin-top:10px;
      font-size:12px;
      opacity:0.8;
    }

    .progress-container{
      margin-top:15px;
      width:100%;
      height:12px;
      background:rgba(255,255,255,.3);
      border-radius:20px;
      overflow:hidden;
    }

    .progress-bar{
      height:100%;
      width:0%;
      background:#ffffff;
      transition:width .3s ease;
    }

    .upload-btn:disabled{
      opacity:.7;
      cursor:not-allowed;
    }
</style>