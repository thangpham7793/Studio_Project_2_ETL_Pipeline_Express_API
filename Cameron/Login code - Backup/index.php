<?php
  require "login_header.php";
 ?>

 <main>
    <div class="map-container" id="map"></div>
    <div class="sidebar">
      <input class="sidebar_input" id="inputAddress" type="text" placeholder="Delivery address...">
      <input class="sidebar_input" id="inputMaterial"l type="text" list="materialList" onkeyup="searchMaterial(this.value)" placeholder="Material/SIC code...">
      <datalist id="materialList"></datalist>
      <label for="formControlRange">Search radius:</label>
      <div class="d-flex justify-content-center my-4">
        <input type="range" class="custom-range" id="sliderSearchRadius" min="10" max="100" step="10" value="20" onchange="updateRangeValue(this.value)" oninput="updateRangeValue(this.value)">
        <span class="font-weight-bold text-primary ml-2 valueSpan2" id="searchRadiusDisplay">20</span>
      </div>
      <button type="button" class="btn btn-primary mb-2">Search</button>
    </div>
 </main>

 <?php
   require "end_file.php";
  ?>
