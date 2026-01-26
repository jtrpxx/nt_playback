<template>
  <MainLayout>
    <div class="main-wrapper-container">
      <div class="card">
        <div class="card-body">
          <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px">
            <div class="d-flex align-items-center">
              <div class="d-flex align-items-center justify-content-center me-1" style="width: 35px; height: 35px; background-color: #d9e2f6; border-radius: 10px !important">
                <i class="fas fa-shield-alt" style="color: #2b6cb0; font-size: 18px"></i>
              </div>
              <h5 class="card-title mb-2 mt-1">Base Roles</h5>
            </div>
          </div>

          <div class="roles-grid" id="baseRolesGrid">
            <div class="role-box" data-role="1">
              <div class="role-box-header">
                <div class="role-box-icon">
                  <i class="fas fa-crown"></i>
                </div>
                <span class="role-box-badge">Click to edit</span>
              </div>
              <div class="role-box-name">Administrator</div>
              <div class="role-box-desc">Full system access</div>
            </div>
            <div class="role-box" data-role="2">
              <div class="role-box-header">
                <div class="role-box-icon">
                  <i class="fas fa-clipboard-check"></i>
                </div>
                <span class="role-box-badge">Click to edit</span>
              </div>
              <div class="role-box-name">Auditor</div>
              <div class="role-box-desc">Read & audit access</div>
            </div>
            <div class="role-box" data-role="3">
              <div class="role-box-header">
                <div class="role-box-icon">
                  <i class="fas fa-headset"></i>
                </div>
                <span class="role-box-badge">Click to edit</span>
              </div>
              <div class="role-box-name">Operator/Agent</div>
              <div class="role-box-desc">Standard operations</div>
            </div>
          </div>
        </div>
      </div>

      <div class="card card-custom-role">
        <div class="card-body">
          <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px">
            <div class="d-flex align-items-center">
              <div class="d-flex align-items-center justify-content-center me-1" style="width: 35px; height: 35px; background-color: #d9e2f6; border-radius: 10px !important">
                <i class="fas fa-shield-alt" style="color: #2b6cb0; font-size: 18px"></i>
              </div>
              <h5 class="card-title mb-2 mt-1">Base Roles</h5>
            </div>
            <div style="display: flex; align-items: center; gap: 10px">
              <div data-v-2dc54a20="" class="search-group" style="width: 260px; position: relative">
                <i data-v-2dc54a20="" class="fa-solid fa-magnifying-glass search-icon"></i>
                <input data-v-2dc54a20="" type="text" class="form-control form-control-sm search-input" placeholder="Search..." fdprocessedid="lf0zjn" />
              </div>
              <button type="button" class="btn-role btn-primary btn-sm" id="addRoleBtn">
                <i class="fas fa-plus"></i>
                Add New Role
              </button>
            </div>
          </div>

          <div class="custom-roles-list" id="customRolesList">
            <div class="custom-role-item" data-index="{{ role.id }}" onclick="openEditRoleModal('{{ role.id }}')">
              <div class="custom-role-info">
                <div class="custom-role-name">sdsdsd</div>
                <span class="custom-role-perms">Permissions</span>
              </div>
              <div class="custom-role-actions">
                <span class="role-box-badge">Click to edit</span>
                <button type="button" class="group-delete-btn" onclick="deleteCustomRole('{{ role.id }}'); event.stopPropagation();" title="Delete Role">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>

            <div class="empty-state">
              <i class="fas fa-user-plus"></i>
              <p>No custom roles yet. Click "Add New Role" to create one.</p>
            </div>
            <div class="empty-state" id="noSearchResults" style="display: none">
              <i class="fa-solid fa-dove"></i>
              <p>No roles found matching your search.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>
<script setup>
import MainLayout from "../layouts/MainLayout.vue";
</script>
