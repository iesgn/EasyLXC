%include('header.tpl')
<body class="hold-transition skin-blue sidebar-mini">
<div class="wrapper">
  <header class="main-header">
    <a href="/inicio" class="logo">
      <span class="logo-lg"><img src="/static/images/logo.png"></span>
    </a>
  </header>
  <aside class="main-sidebar">
    <section class="sidebar">
      <ul class="sidebar-menu" data-widget="tree">
	<li class="header">UPTIME</li>
	<li class="treeview">
	  <a href="/inicio">
	    <i class="fa fa-arrow-up"></i> <span>{{ uptime }}</span>
	  </a>
	</li>
      </ul>
      <ul class="sidebar-menu" data-widget="tree">
        <li class="header">MENÚ</li>
        <li class="active treeview">
          <a href="/">
	    <i class="fa fa-window-maximize"></i>Página principal</a>
	  </a>
        </li>
	</a>
        <li class="treeview">
                <li><a href="/contenedores"><i class="fa fa-cubes"></i>Contenedores</a></li>
        </li>
	<li class="treeview">
                <li><a href="/snapshots"><i class="fa fa-camera-retro"></i>Snapshots</a></li>
        </li>
<li class="treeview">
	  <li><a href="/monitor"><i class="fa fa-dashboard"></i>Monitorización de Ping</a></li>
	</li>
      </ul>
    </section>
  </aside>
  <div class="content-wrapper">
    <section class="content-header">
      <h1>
        Dashboard
      </h1>
      <ol class="breadcrumb">
        <li><a href="/"><i class="fa fa-dashboard"></i> Home</a></li>
        <li class="active">Principal</li>
      </ol>
    </section>
    <section class="content">
      <h1>
        Información de contenedores
      </h1>
      <div class="row">
        <div class="col-md-4">
          <div class="small-box bg-light-blue color-palette">
            <div class="inner">
              <h3>{{ total }}</h3>

              <p>Total de contenedores</p>
            </div>
            <a href="/contenedores" class="small-box-footer">Ver todos los contenedores <i class="fa fa-arrow-circle-right"></i></a>
          </div>
        </div>
	<div class="col-md-4">
          <div class="small-box bg-green">
            <div class="inner">
              <h3>{{ activos }}</h3>

              <p>Contenedores activos</p>
            </div>
            <div class="icon">
              <i class="ion ion-arrow-up-b"></i>
            </div>
            <a href="/contenedores" class="small-box-footer">Ver todos los contenedores <i class="fa fa-arrow-circle-right"></i></a>
          </div>
        </div>
        <div class="col-md-4">
          <div class="small-box bg-red">
            <div class="inner">
              <h3>{{ apagados }}</h3>

              <p>Contenedores apagados</p>
            </div>
            <div class="icon">
              <i class="ion ion-arrow-down-b"></i>
            </div>
            <a href="/contenedores" class="small-box-footer">Ver todos los contenedores <i class="fa fa-arrow-circle-right"></i></a>
          </div>
        </div>
      </div>
      <h1>
        Información de los recursos del anfitrión
      </h1>
      <div class="callout callout-default">
        <h4>{{ modelprocessor }}</h4>

        <p>Modelo del procesador</p>
      </div>
      <div class="row">
        <div class="col-lg-3 col-xs-6">
          <div class="small-box bg-light-blue color-palette">
            <div class="inner">
              <h3>{{ ramtotal }}M</h3>

              <p>Memoria RAM total del anfitrión</p>
            </div>
          </div>
        </div>
	% if ramused > limiteram:
          <div class="col-lg-3 col-xs-6">
            <div class="small-box bg-red">
              <div class="inner">
                <h3>{{ ramused }}M</h3>

                <p>Memoria RAM usada</p>
              </div>
            </div>
          </div>
	% else:
	  <div class="col-lg-3 col-xs-6">
            <div class="small-box bg-green">
              <div class="inner">
                <h3>{{ ramused }}M</h3>

                <p>Memoria RAM usada</p>
              </div>
            </div>
          </div>
	% end
        <div class="col-lg-3 col-xs-6">
          <div class="small-box bg-light-blue color-palette">
            <div class="inner">
              <h3>{{ disktotal }}G</h3>

              <p>Espacio de disco total del anfitrión</p>
            </div>
          </div>
        </div>
        % if diskused > limitedisk:
          <div class="col-lg-3 col-xs-6">
            <div class="small-box bg-red">
              <div class="inner">
                <h3>{{ diskused }}</h3>

                <p>Espacio de disco usado del anfitrión</p>
              </div>
            </div>
          </div>
        % else:
          <div class="col-lg-3 col-xs-6">
            <div class="small-box bg-green">
              <div class="inner">
                <h3>{{ diskused }}</h3>

                <p>Espacio de disco usado del anfitrión</p>
              </div>
            </div>
          </div>
        % end
      </div>
    </section>
  </div>
</script>
%include('foot.tpl')
