import * as THREE from 'three';

// init basis for the scene
const container = document.getElementById( 'container' );
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

// color the background
scene.background = new THREE.Color( 'rgb(255, 255, 255)' );
scene.add( camera );

// setup the renderer
const renderer = new THREE.WebGLRenderer();
renderer.setPixelRatio( window.devicePixelRatio );
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Soft shadows

container.appendChild( renderer.domElement );

// Create a plane to receive shadows
const floor_geometry = new THREE.PlaneGeometry(100, 100);
const floor_material = new THREE.MeshStandardMaterial({
  color: 'rgb(255, 255, 255)', // Gray color
  roughness: 1,    // Matte surface
});
const floor = new THREE.Mesh(floor_geometry, floor_material);
floor.rotation.x = -Math.PI / 2; // Rotate to be horizontal
floor.receiveShadow = true; // Allow shadows on it
scene.add(floor);

// add a grid 
const viz_grid = new THREE.GridHelper(100, 100, 'rgb(245, 3, 3)', 'rgb(0, 0, 0)');
viz_grid.position.y = 0.1; // Lift it slightly to prevent Z-fighting
scene.add(viz_grid);

// Add lighting
const sky_light = new THREE.HemisphereLight(0xffffff, 0x444444, 1.5);
scene.add(sky_light);



// Create sphere
const sphere_geometry = new THREE.SphereGeometry(1, 32, 32);
const sphere_material = new THREE.MeshStandardMaterial({ color: 'rgb(88, 130, 208)' });
const sphere = new THREE.Mesh(sphere_geometry, sphere_material);
sphere.position.set(0, 4, 0); // Offset the camera behind the sphere
sphere.castShadow = true;

const camera_sphere = new THREE.Object3D();
camera_sphere.position.set(0, 9, 20); // Offset the camera behind the sphere
sphere.add(camera_sphere);

// Create cone (pointing downward)
const cone_geometry = new THREE.ConeGeometry(0.8, 1.0, 32);
const cone_material = new THREE.MeshStandardMaterial({ color: 'rgb(163, 35, 222)' });
const cone = new THREE.Mesh(cone_geometry, cone_material);
// Adjust cone position and rotation
cone.position.set(0, -1.8, 0); // Move cone down below the sphere
cone.rotation.x = Math.PI; // Rotate 180° to point downward
sphere.add(cone);

// Directional Light (Casts Shadows)
const spot_light = new THREE.SpotLight(0xffffff, 200);
spot_light.position.set(0, 15, 0);
spot_light.castShadow = true;
spot_light.shadow.mapSize.width = 1024;
spot_light.shadow.mapSize.height = 1024;
spot_light.shadow.camera.near = 0.5;
spot_light.shadow.camera.far = 100;
spot_light.target = sphere;
sphere.add(spot_light);

scene.add(sphere);

// Update the third-person camera position
function updateCameraPosition() {
  camera.position.copy(camera_sphere.getWorldPosition(new THREE.Vector3()));
  camera.lookAt(sphere.position);

}

function updateAgentPosition() {
  // Rotate objects for effect
  sphere.position.x += Math.sin(t) * motion_speed;
  sphere.position.z += Math.cos(t) * motion_speed;
}

const motion_speed = 0.2;
let t = 0;
// Animation loop
function animate() {
  t += 1.0 / 60.0;
  requestAnimationFrame(animate);

  updateAgentPosition();
  updateCameraPosition();
  renderer.render(scene, camera);
}

animate();
