<?php
  require "login_header.php";
 ?>

 <main>
    <div class="map-container" id="map"></div>
    <div class="sidebar">
      <p>Click map to set location</p>
      <input class="sidebar_input" id="inputAddress" type="text" placeholder="Click to set location" onkeyup="enableSearch()">
      <input class="sidebar_input" id="inputMaterial" type="text" list="materialList" placeholder="All Material" onkeyup="updateSearch()">
      <datalist id="materialList">
      </datalist>
      <label for="formControlRange">Search radius (miles):</label>
      <div class="d-flex justify-content-center my-4">
        <input type="range" class="custom-range" id="sliderSearchRadius" min="10" max="200" step="10" value="50" onchange="updateRangeValue(this.value)" oninput="updateRangeValue(this.value)">
        <span class="font-weight-bold text-primary ml-2 valueSpan2" id="searchRadiusDisplay">50</span>
      </div>
      <button type="button" id="btnSearch" class="btn btn-primary mb-2" onclick="searchForSupplier()">Search</button>
    </div>
 </main>

 <?php
   require "end_file.php";
  ?>
