import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { TransformControls } from 'three/addons/controls/TransformControls.js';
import axios from 'axios';

const container = document.getElementById( 'container' );

const scene = new THREE.Scene();
scene.background = new THREE.Color( 0xf0f0f0 );

const camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 1, 10000 );
camera.position.set( 15, 8, 10 );
camera.rotation.set( 0, Math.PI / 2, 0 );
scene.add( camera );

scene.add( new THREE.AmbientLight( 0xf0f0f0, 3 ) );
const light = new THREE.SpotLight( 0xffffff, 4.5 );
light.position.set( 0, 1500, 200 );
light.angle = Math.PI * 0.2;
light.decay = 0;
light.castShadow = true;
light.shadow.camera.near = 200;
light.shadow.camera.far = 2000;
light.shadow.bias = - 0.000222;
light.shadow.mapSize.width = 1024;
light.shadow.mapSize.height = 1024;
scene.add( light );

const planeGeometry = new THREE.PlaneGeometry( 2000, 2000 );
planeGeometry.rotateX( - Math.PI / 2 );
const planeMaterial = new THREE.ShadowMaterial( { color: 0x000000, opacity: 0.2 } );

const plane = new THREE.Mesh( planeGeometry, planeMaterial );
plane.position.y = 0;
plane.receiveShadow = true;
scene.add( plane );

const helper = new THREE.GridHelper( 2000, 100 );
helper.position.y = 1;
helper.material.opacity = 0.25;
helper.material.transparent = true;
scene.add( helper );

const renderer = new THREE.WebGLRenderer( { antialias: true } );
renderer.setPixelRatio( window.devicePixelRatio );
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.shadowMap.enabled = true;
container.appendChild( renderer.domElement );

// Controls
// const controls = new OrbitControls( camera, renderer.domElement );
// controls.damping = 0.2;
// controls.addEventListener( 'change', animate);
// const transformControl = new TransformControls( camera, renderer.domElement );
// transformControl.addEventListener( 'change', animate );
// transformControl.addEventListener( 'dragging-changed', function ( event ) {

//   controls.enabled = ! event.value;

// } );
// scene.add( transformControl.getHelper() );

const gate_geometry = new THREE.RingGeometry( 2, 3, 4 ); 
const gate_material = new THREE.MeshBasicMaterial( { color: 'rgb(65, 65, 214)', side: THREE.DoubleSide } );
const gate = new THREE.Mesh( gate_geometry, gate_material );
gate.position.y = 10;
gate.rotation.z = Math.PI / 4.0;
scene.add( gate );

// Create cone 
const cone_geometry = new THREE.ConeGeometry(0.1, 0.3, 32);
const cone_material = new THREE.MeshStandardMaterial({ color: 'rgb(222, 69, 35)' });
const cone = new THREE.Mesh(cone_geometry, cone_material);
// Adjust cone position and rotation
cone.position.set(-2, 10, 0); // Move cone down below the sphere
cone.rotation.x = Math.PI / 2; // Rotate 180° to point downward
scene.add(cone);

// Line trail setup
const trail_size = 1000; // Number of points in the trail
const trail_points = new Float32Array(trail_size * 3); // 3 values per point (x, y, z)
const trail_geometry = new THREE.BufferGeometry();
trail_geometry.setAttribute("position", new THREE.BufferAttribute(trail_points, 3));
const trail_material = new THREE.LineBasicMaterial({ color: 'rgb(255, 102, 0)' });
const trail = new THREE.Line(trail_geometry, trail_material);
scene.add(trail);

function updateTrail() {
  // Update trail positions
  for (let i = trail_size - 1; i > 0; i--) {
    trail_points[i * 3] = trail_points[(i - 1) * 3];     // x
    trail_points[i * 3 + 1] = trail_points[(i - 1) * 3 + 1]; // y
    trail_points[i * 3 + 2] = trail_points[(i - 1) * 3 + 2]; // z
  }

  // Set new trail position at index 0
  trail_points[0] = cone.position.x;
  trail_points[1] = cone.position.y;
  trail_points[2] = cone.position.z;

  trail_geometry.attributes.position.needsUpdate = true;
}

interface Vector3 {
  x: number;
  y: number;
  z: number;
}

function updateConePosition(position: Vector3) {
  console.log(position.x);
  cone.position.set(position.x, position.y, position.z);
}

// Animation loop
function animate() {
axios.get<Vector3>('http://127.0.0.1:5000/app/data')
  .then((response: { data: Vector3; }) => updateConePosition(response.data))
  .catch((error: any) => console.error('Error:', error));
  requestAnimationFrame(animate);

  updateTrail();
  renderer.render(scene, camera);
}

animate();
