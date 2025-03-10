import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { TransformControls } from 'three/addons/controls/TransformControls.js';
import axios from 'axios';


interface Vector3 {
  x: number;
  y: number;
  z: number;
}

const scene = new THREE.Scene();
scene.background = new THREE.Color( 0xf0f0f0 );

const camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 1, 10000 );
camera.position.set( 15, 8, 10 );
camera.rotation.set( 0, Math.PI / 2, 0 );
// camera.position.set( 0, 8, 20 );
// camera.rotation.set( -Math.PI / 2, 0, 0 );
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

const container = document.getElementById( 'container' );
container.appendChild( renderer.domElement );

// Controls
const controls = new OrbitControls( camera, renderer.domElement );
controls.damping = 0.2;
controls.addEventListener( 'change', animate);
const transformControl = new TransformControls( camera, renderer.domElement );
transformControl.addEventListener( 'change', animate );
transformControl.addEventListener( 'dragging-changed', function ( event ) {
  controls.enabled = ! event.value;

} );
scene.add( transformControl.getHelper() );

const gate_geometry = new THREE.RingGeometry( Math.sqrt(2), 2 * Math.sqrt(2), 4 ); 
const gate_material = new THREE.MeshBasicMaterial( { color: 'rgb(65, 65, 214)', side: THREE.DoubleSide } );
const gate = new THREE.Mesh( gate_geometry, gate_material );
gate.position.y = 10;
gate.rotation.y = Math.PI / 2.0;
gate.rotation.z = Math.PI / 4.0;
scene.add( gate );

const particle_count = 100; // Number of points in the trail
const trail_size = 100; // Numbaer of points in the trail
const trail_colors = [];
for (let index = 0; index < trail_size; index++) {
  trail_colors.push(new THREE.Color().setRGB( 1.0, (1.0 / trail_size) * index, (1.0 / trail_size) * index));
}

const particle_geometry = new THREE.SphereGeometry(0.05);
const particle_material = new THREE.MeshStandardMaterial({ color: 'rgb(227, 69, 45)' });
const particle_mesh = new THREE.InstancedMesh(particle_geometry, particle_material, particle_count * trail_size);
scene.add(particle_mesh);

function updateParticleTrail(particle_index: number, trail_size: number, cur_position: Vector3) {
  for (let i = trail_size - 1; i > 0; i--) {
    let tmp_matrix = new THREE.Matrix4();
    particle_mesh.getMatrixAt(particle_index + i - 1, tmp_matrix);
    particle_mesh.setMatrixAt(particle_index + i, tmp_matrix);
  }
  const dummy = new THREE.Object3D();
  dummy.position.set(cur_position.x, cur_position.y, cur_position.z); // Move cone down below the sphere
  dummy.updateMatrix();

  particle_mesh.setMatrixAt(particle_index, dummy.matrix);
}

function updateParticles(positions: Array<Vector3>) {
  for (let i = 0; i < particle_count; i++) {
    updateParticleTrail(i * trail_size, trail_size, positions[i]);
  }

  particle_mesh.instanceMatrix.needsUpdate = true;
}

function animate() {
axios.get<Array<Vector3>>('http://127.0.0.1:5000/app/data')
  .then((response: { data: Array<Vector3>; }) => updateParticles(response.data))
  .catch((error: any) => console.error('Error:', error));
  requestAnimationFrame(animate);

  // updateTrail();
  renderer.render(scene, camera);
}

animate();
