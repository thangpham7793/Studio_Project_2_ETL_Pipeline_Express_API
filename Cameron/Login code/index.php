<?php
  require "login_header.php";
 ?>
 <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDYso3RVo8lv770AknwyoaH_Bq8tr2CSr4&libraries=&v=weekly" defer ></script>
 <main>
    <div class="map-container" id="map"></div>

    <!-- Sidebar -->
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
    <!-- End Sidebar -->

    <!-- Modal -->
    <div class="modal fade" id="modal_request_price">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Request Price</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>

          <!-- Request modal -->
          <form id="formRequestPrice" action="includes/request_submit.inc.php" method="post">
          <div class="modal-body">
               <div class="form-row">
                 <div class="form-group col-md-6">
                   <label for="inputRequestFirstName">First Name</label>
                   <input type="text" name="firstName" class="form-control" id="inputRequestFirstName" placeholder="First name...">
                 </div>
                 <div class="form-group col-md-6">
                   <label for="inputRequestSurname">Surname</label>
                   <input type="text" name="surname" class="form-control" id="inputRequestSurname" placeholder="Surname...">
                 </div>
               </div>
               <div class="form-row">
                 <div class="form-group col-md-6">
                   <label for="inputRequestPhone">Phone</label>
                   <input type="text" name="phone" class="form-control" id="inputRequestPhone" placeholder="Phone...">
                 </div>
                 <div class="form-group col-md-6">
                   <label for="inputRequestEmail">Email</label>
                   <input type="text" name="email" class="form-control" id="inputRequestEmail" placeholder="Email...">
                 </div>
               </div>
               <div class="form-group">
                 <label for="inputRequestAddress">Delivery Address</label>
                 <textarea name="address" class="form-control" id="inputRequestAddress" placeholder="Address..."></textarea>
               </div>
               <div class="form-group">
                 <label for="inputRequestMaterials">Materials</label>
                 <textarea name="materials" class="form-control" id="inputRequestMaterials" placeholder="Materials..."></textarea>
               </div>
               <div class="form-group">
                 <label for="inputRequestAddDetails">Additional Details</label>
                 <textarea name="addDetails" class="form-control" id="inputRequestAddDetails" placeholder="Additional Details..."></textarea
               </div>
               <p id="submitRequest-feedback"></p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="submit" name="request-submit" class="btn btn-primary">Submit</button>
          </div>
          </form>
        </div>
      </div>
    </div>
    <!-- End modal -->

 </main>

 <?php
   require "end_file.php";
  ?>
